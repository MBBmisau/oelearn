from django import dispatch
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.apps import apps
from academic.mixins import CurrentBatchLiveMixin

from course.models import Course, Module
from dashboard import exam
from result.mixins import ResultReleaseForbiddenMixin
from .models import CA, Exam, StudentCompletedCA, StudentCompletedExam
from result.models import StudentCAQuestion, StudentExam, StudentResult, StudentCA, StudentExamQuestion
from academic.utils import get_current_batch
from student.mixins import StudentTestMixin
from course.mixins import StudentCourseMixin
from .mixins import ExamOpenMixin

BATCH = get_current_batch()

class TakeCA(StudentTestMixin, StudentCourseMixin, CurrentBatchLiveMixin, ResultReleaseForbiddenMixin, TemplateView):
    #module_id,paper_model,pk
    #get exam get appropriet model
    #pass forrm in get
    #accept form in get and create student question as well as CA
    #mark obj and leave other unmark
    def get_model(self, paper_model):
        if paper_model in ['objective', 'essay', 'assignment']:
            return apps.get_model(app_label='exam', model_name=paper_model)
        return None

    def dispatch(self, request, ca_id, module_id, paper_model, pk):
        self.student = request.user.student
        self.module = get_object_or_404(Module, id=module_id)
        self.paper_model = paper_model
        self.course = self.module.course
        self.paper = self.get_model(paper_model)
        self.ca_paper = get_object_or_404(self.paper, pk=pk)
        self.ca = get_object_or_404(CA, id=ca_id)
        self.batch = BATCH
        self.validation = StudentCompletedCA.objects.get_or_create(student=self.student,ca=self.ca,batch=self.batch)[0]
        self.redirect_to = reverse('course:course_detail', kwargs={'module_id': self.module.id})
        if not self.ca_paper == self.ca.paper:
            raise PermissionDenied()
        if not paper_model == 'assignment':
            if request.method == 'GET' and self.validation.completed >= StudentCompletedCA.COMPLETED_GET:
                messages.info(request, 'You have already load this assessment.')
                return redirect(self.redirect_to)
        if request.method == 'GET' and self.validation.completed == StudentCompletedCA.COMPLETED_POST:
            messages.info(request, 'You have already submitted this assessment.')
            return redirect(self.redirect_to)
        if request.method == 'POST' and self.validation.completed == StudentCompletedCA.COMPLETED_POST:
            messages.info(request, 'You have already submitted this assessment.')
            return redirect(self.redirect_to)
        return super().dispatch(request, ca_id, module_id, paper_model, pk)

    def get(self, request, *args, **kwargs):
        if not self.ca.live:
            messages.error(request, 'This CA is temporarily Unavailable!')
            return redirect(self.redirect_to)
        self.validation.completed = StudentCompletedCA.COMPLETED_GET
        self.validation.save()
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.paper_model == 'objective':
            self.template_name = 'exam/objective.html'
        elif self.paper_model =='essay':
            self.template_name = 'exam/essay.html'
        elif self.paper_model == 'assignment':
            self.template_name = 'exam/assignment.html'
        return super().get_template_names()

    def post(self, request, paper_model, *args, **kwargs):
        student_ca = StudentCA.objects.get_or_create(student=self.student,ca=self.ca,batch=self.batch,module=self.module,course=self.course)[0]
        for question in self.ca_paper.questions.all():
            student_question = StudentCAQuestion(student_ca=student_ca,question=question,max_possible_score=question.marks)
            student_question.save()
        #    student_ca.questions.add(student_question)
        #    student_ca.save()
        ca_max_marks = 0
        student_q_list = student_ca.questions.all()
        paper_q_list = self.ca_paper.questions.all()
        i = 0
        for qi in range(paper_q_list.count()):
            ques = student_q_list[qi]
            #for question in self.ca_paper.questions.all():
            max_marks = paper_q_list[i].marks
            ans = request.POST.get(ques.question.question, False)
            ques.max_possible_score = max_marks
            ques.student_answer = ans
            ques.save()
            ca_max_marks += max_marks
            i += 1
        student_ca.max_possible_score = ca_max_marks
        student_ca.save()
        if self.paper_model == 'objective':
            ca_score = 0
            student_q_list = student_ca.questions.all()
            paper_q_list = self.ca_paper.questions.all()
            i = 0
            for qi in range(paper_q_list.count()):
                ques = student_q_list[qi]
                max_marks = paper_q_list[i].marks
                answer = ques.student_answer
                paper_q_ans = paper_q_list[i].answer
                if answer:
                    if answer.lower() == paper_q_ans.lower() or answer == paper_q_ans:
                        ques.score = max_marks
                        ques.save()
                        ca_score += max_marks
                    else:
                        ques.score = 0
                        ques.save()
                    i += 1
            student_ca.score = ca_score
            student_ca.marked = True
            student_ca.save()
            result = StudentResult.objects.get_or_create(student=self.student,batch=self.batch,course=self.course)[0]
            #result.cas.add(student_ca)
            #result.save()
            messages.success(request, f'Assessment submitted successfully! Your score is {student_ca.score}/{student_ca.max_possible_score}')
            return redirect(self.redirect_to)
        messages.success(request, 'Assessment successfully submitted for marking.')
        return redirect(self.redirect_to)

    def convert(self, seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        min += hour*60
        return "%02d:%02d" % (min, sec)

    #def get(self, request, paper_model):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        student = self.request.user.student
        context['student'] = student
        context['paper'] = self.ca_paper
        context['questions'] = self.ca.paper.questions.all()
        context['module'] = self.module
        context['course'] = self.course
        context['batch'] = self.batch
        if self.paper_model == 'essay' or self.paper_model == 'objective':
            time_delta = self.ca_paper.end_time - self.ca_paper.start_time
            time = self.convert(time_delta.seconds)
            time = time.split(":")
            context['mins'] = time[0]
            context['secs'] = time[1]
        return context

class CourseExamIndex(StudentTestMixin, StudentCourseMixin, ExamOpenMixin, TemplateView):
    template_name = 'exam/course_exam_index.html'

    def dispatch(self, request, course_id, *args, **kwargs):
        self.course = get_object_or_404(Course, id=course_id)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        context['exams'] = Exam.objects.filter(live=True)
        return context
    

class TakeExam(StudentTestMixin, StudentCourseMixin, CurrentBatchLiveMixin, ExamOpenMixin, ResultReleaseForbiddenMixin, TemplateView):
    #module_id,paper_model,pk
    #get exam get appropriet model
    #pass forrm in get
    #accept form in get and create student question as well as CA
    #mark obj and leave other unmark
    def get_model(self, paper_model):
        if paper_model in ['objective', 'essay', 'assignment']:
            return apps.get_model(app_label='exam', model_name=paper_model)
        return None

    def dispatch(self, request, exam_id, course_id, paper_model, pk):
        self.student = request.user.student
        self.course = get_object_or_404(Course, id=course_id)
        self.paper_model = paper_model
        self.paper = self.get_model(paper_model)
        self.exam_paper = get_object_or_404(self.paper, pk=pk)
        self.exam = get_object_or_404(Exam, id=exam_id)
        self.batch = BATCH
        self.validation = StudentCompletedExam.objects.get_or_create(student=self.student,exam=self.exam,batch=self.batch)[0]
        self.redirect_to = reverse('exam:course_exam_index', kwargs={'course_id':self.course.id})
        if not self.exam_paper == self.exam.paper:
            raise PermissionDenied()
        if request.method == 'GET' and self.validation.completed >= StudentCompletedExam.COMPLETED_GET:
            messages.info(request, 'You have already load this Exam.')
            return redirect(self.redirect_to)
        if request.method == 'GET' and self.validation.completed == StudentCompletedExam.COMPLETED_POST:
            messages.info(request, 'You have already submitted this Exam.')
            return redirect(self.redirect_to)
        if request.method == 'POST' and self.validation.completed == StudentCompletedExam.COMPLETED_POST:
            messages.info(request, 'You have already submitted this Exam.')
            return redirect(self.redirect_to)
        return super().dispatch(request, exam_id, course_id, paper_model, pk)

    def get(self, request, *args, **kwargs):
        if not self.exam.live:
            messages.error(request, 'This Exam is temporarily Unavailable!')
            return redirect(self.redirect_to)
        self.validation.completed = StudentCompletedCA.COMPLETED_GET
        self.validation.save()
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.paper_model == 'objective':
            self.template_name = 'exam/objective.html'
        elif self.paper_model =='essay':
            self.template_name = 'exam/essay.html'
        return super().get_template_names()

    def post(self, request, paper_model, *args, **kwargs):
        student_exam = StudentExam.objects.get_or_create(student=self.student,exam=self.exam,batch=self.batch,course=self.course)[0]
        for question in self.exam_paper.questions.all():
            student_question = StudentExamQuestion(student_exam=student_exam,question=question,max_possible_score=question.marks)
            student_question.save()
        #    student_ca.questions.add(student_question)
        #    student_ca.save()
        exam_max_marks = 0
        student_q_list = student_exam.questions.all()
        paper_q_list = self.exam_paper.questions.all()
        i = 0
        for qi in range(paper_q_list.count()):
            ques = student_q_list[qi]
            #for question in self.ca_paper.questions.all():
            max_marks = paper_q_list[i].marks
            ans = request.POST.get(ques.question.question, False)
            ques.max_possible_score = max_marks
            ques.student_answer = ans
            ques.save()
            exam_max_marks += max_marks
            i += 1
        student_exam.max_possible_score = exam_max_marks
        student_exam.save()
        if self.paper_model == 'objective':
            exam_score = 0
            student_q_list = student_exam.questions.all()
            paper_q_list = self.exam_paper.questions.all()
            i = 0
            for qi in range(paper_q_list.count()):
                ques = student_q_list[qi]
                max_marks = paper_q_list[i].marks
                answer = ques.student_answer
                paper_q_ans = paper_q_list[i].answer
                if answer:
                    if answer.lower() == paper_q_ans.lower() or answer == paper_q_ans:
                        ques.score = max_marks
                        ques.save()
                        exam_score += max_marks
                    else:
                        ques.score = 0
                        ques.save()
                    i += 1
            student_exam.score = exam_score
            student_exam.marked = True
            student_exam.save()
            #result = StudentResult.objects.get_or_create(student=self.student,batch=self.batch,course=self.course)[0]
            #result.exams.add(student_exam)
            result.save()
            messages.success(request, f'Exam submitted successfully! Your score is {student_exam.score}/{student_exam.max_possible_score}')
            return redirect(self.redirect_to)
        messages.success(request, 'Exam successfully submitted for marking.')
        return redirect(self.redirect_to)

    def convert(self, seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        min += hour*60
        return "%02d:%02d" % (min, sec)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        student = self.request.user.student
        context['student'] = student
        context['paper'] = self.exam_paper
        context['questions'] = self.exam.paper.questions.all()
        context['course'] = self.course
        context['batch'] = self.batch
        time_delta = self.exam_paper.end_time - self.exam_paper.start_time
        time = self.convert(time_delta.seconds)
        time = time.split(":")
        context['mins'] = time[0]
        context['secs'] = time[1]
        return context