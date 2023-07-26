from platform import release
from django.conf import settings

from academic.utils import get_current_batch
from result.models import ResultRelease, StudentCA, StudentExam, StudentResult

BATCH = get_current_batch()

def is_result_released(batch=BATCH):
    try:
        release = ResultRelease.objects.get(batch=batch)
        if release.released:
            return True
        return False
    except:
        return False

def get_total_for_exam(course):
    total = 0
    for exam in course.exams.filter(live=True):
        total += exam.paper.total_marks
    return total

def get_total_for_ca(course):
    total = 0
    for module in course.modules.all():
        for ca in module.assessments.filter(live=True):
            total += ca.paper.total_marks
    return total

def get_student_exams(course, student):
    return StudentExam.objects.filter(exam__live=True,course=course,student=student,batch=BATCH)

def get_student_total_for_exam(course, student):
    student_total = 0
    exams = get_student_exams(course, student)
    student_result = StudentResult.objects.get_or_create(student=student,course=course,batch=BATCH)[0]
    for exam in exams:
        student_total += exam.score
        student_result.exams.add(exam)
    return student_total

def get_student_total_for_ca(course, student):
    student_total = 0
    cas = StudentCA.objects.filter(course=course,student=student,batch=BATCH,course__live=True)
    student_result = StudentResult.objects.get_or_create(student=student,course=course,batch=BATCH)[0]
    for ca in cas:
        student_total += ca.score
        student_result.cas.add(ca)
    return student_total

def get_student_exam_score(exam_total, student_exam_total):
    #return student score currently over 70
    mark_allocation = settings.EXAM_MARK_ALLOCATION
    return (student_exam_total * mark_allocation) / exam_total

def get_student_ca_score(ca_total, student_ca_total):
    #return student score currently over 70
    mark_allocation = settings.CA_MARK_ALLOCATION
    return (student_ca_total * mark_allocation) / ca_total

def generate_result(course):
    exam_total = get_total_for_exam(course)
    ca_total = get_total_for_ca(course)
    for student in course.students.all():
        student_exam_total = get_student_total_for_exam(course, student)
        student_ca_total = get_student_total_for_ca(course, student)
        student_exam_score = get_student_exam_score(exam_total, student_exam_total)
        student_ca_score = get_student_ca_score(ca_total, student_ca_total)
        student_result = StudentResult.objects.get_or_create(student=student,course=course,batch=BATCH)[0]
        student_result.total_exam_score = student_exam_score
        student_result.total_ca_score = student_ca_score
        student_result.save()
        released = ResultRelease.objects.get_or_create(batch=BATCH)