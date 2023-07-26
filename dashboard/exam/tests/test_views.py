from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from dashboard import exam

from dashboard.tests.test_views import DashboardAdminTestCase, DashboardAdminOrInstructorTestCase
from exam.models import Exam, CA, Objective, ObjectiveQuestion, Essay, EssayQuestion, Assignment, AssignmentQuestion
from course.models import Course, Module, Subject

class AddCATest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:add_ca', kwargs={'module_id': 1,'model_name':'essay'}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:add_ca', kwargs={'module_id': 1,'model_name':'essay'}))
        self.assertEqual(response.status_code, 200)

class EditCATest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        essay_paper = Essay.objects.create(title='First essay')
        ca = CA.objects.create(module=module,paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:edit_ca', kwargs={'module_id': 1,'model_name':'essay','id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:edit_ca', kwargs={'module_id': 1,'model_name':'essay','id':1}))
        self.assertEqual(response.status_code, 200)

class EditCAQuestionTest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        essay_paper = Essay.objects.create(title='First essay')
        ca = CA.objects.create(module=module,paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:edit_ca_question', kwargs={'module_id': 1,'model_name':'essay','paper_id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:edit_ca_question', kwargs={'module_id': 1,'model_name':'essay','paper_id':1}))
        self.assertEqual(response.status_code, 200)

class DeleteCATest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        essay_paper = Essay.objects.create(title='First essay')
        ca = CA.objects.create(module=module,paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:delete_ca', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:delete_ca', kwargs={'pk': 1,}))
        self.assertEqual(response.status_code, 200)

class CourseExamTest(DashboardAdminOrInstructorTestCase):
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:course_exam'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:course_exam'))
        self.assertEqual(response.status_code, 200)

class AddExamTest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:add_exam', kwargs={'course_id': 1,'model_name':'essay'}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:add_exam', kwargs={'course_id': 1,'model_name':'essay'}))
        self.assertEqual(response.status_code, 200)

class EditExamTest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        essay_paper = Essay.objects.create(title='First essay')
        exam = Exam.objects.create(course=course, paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:edit_exam', kwargs={'course_id': 1,'model_name':'essay','id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:edit_exam', kwargs={'module_id': 1,'model_name':'essay','id':1}))
        self.assertEqual(response.status_code, 200)

class EditExamQuestionTest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        essay_paper = Essay.objects.create(title='First essay')
        exam = Exam.objects.create(course=course, paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:edit_exam_question', kwargs={'course_id': 1,'model_name':'essay','paper_id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:edit_exam_question', kwargs={'course_id': 1,'model_name':'essay','paper_id':1}))
        self.assertEqual(response.status_code, 200)

class DeleteExamTest(DashboardAdminOrInstructorTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        essay_paper = Essay.objects.create(title='First essay')
        exam = Exam.objects.create(course=course, paper=essay_paper)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('exam_dashboard:delete_exam', kwargs={'pk': 1,}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('exam_dashboard:delete_exam', kwargs={'pk': 1,}))
        self.assertEqual(response.status_code, 200)