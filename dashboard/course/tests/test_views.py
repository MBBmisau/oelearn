from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from custom_auth.models import CustomUser
from course.models import Subject, Course, Module, Video, Content
from dashboard import course

from dashboard.tests.test_views import DashboardAdminTestCase, DashboardAdminOrInstructorTestCase

class CourseDashboardTest(DashboardAdminTestCase):
    
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:dashboard'))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)

class AddSubjectTest(DashboardAdminTestCase):

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:add_subject'))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/subject/add/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:add_subject'))
        self.assertEqual(response.status_code, 200)

class UpdateSubjectTest(DashboardAdminTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='Math')

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:edit_subject', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/subject/1/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:edit_subject', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class DeleteSubjectTest(DashboardAdminTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='Math')

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:delete_subject', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/subject/1/delete/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:delete_subject', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class AddCourseTest(DashboardAdminTestCase):

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:add_course'))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/add/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:add_course'))
        self.assertEqual(response.status_code, 200)

class UpdateCourseTest(DashboardAdminTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:edit_course', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/1/edit/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:edit_course', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class DeleteCourseTest(DashboardAdminTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)

    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:delete_course', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/1/delete/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:delete_course', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class CourseAddStudentTest(DashboardAdminTestCase):
    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:course_add_student', kwargs={'course_id': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/add/1/student/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:course_add_student', kwargs={'course_id': 1}))
        self.assertEqual(response.status_code, 302)

class EditModule(DashboardAdminOrInstructorTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1', order=1)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:edit_module', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/dashboard/course/1/module/')
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:edit_module', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class AddContentTest(DashboardAdminOrInstructorTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:add_content', kwargs={'module_id': 1,'model_name':'video'}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:edit_module', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

class EditContentTest(DashboardAdminOrInstructorTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        item = Video.objects.create(title='Video object')
        content = Content.objects.create(module=module,item=item)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:edit_content', kwargs={'module_id': 1,'model_name':'video','id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:edit_content', kwargs={'module_id': 1,'model_name':'video','id':1}))
        self.assertEqual(response.status_code, 200)

class DeleteContentTest(DashboardAdminOrInstructorTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        item = Video.objects.create(title='Video object')
        content = Content.objects.create(module=module,item=item)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:delete_content', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:delete_content', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)

class ContentListTest(DashboardAdminOrInstructorTestCase):

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        item = Video.objects.create(title='Video object')
        content = Content.objects.create(module=module,item=item)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:content_list', kwargs={'module_id':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:content_list', kwargs={'module_id':1}))
        self.assertEqual(response.status_code, 200)

class PublishToggleTest(DashboardAdminOrInstructorTestCase):
    #Publish Module content
    #Publish Module CA
    #Publish course exam

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='English')
        instructor = get_user_model().objects.create_user(reg_id='2000', email='inst@gmail.com', user_type=CustomUser.TEACHER)
        course = Course.objects.create(title='Hada baki', instructor=instructor.teacher,subject=subject)
        module = Module.objects.create(course=course,title='Module 1',order=1)
        item = Video.objects.create(title='Video object')
        content = Content.objects.create(module=module,item=item)
        
    def test_redirect_to_if_not_login(self):
        response = self.client.get(reverse('course_dashboard:publish_toggle', kwargs={'model_name':'content','pk':1}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_user_access_dashboard(self):
        login = self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        response = self.client.get(reverse('course_dashboard:content_list', kwargs={'module_id':1}))
        self.assertEqual(response.status_code, 200)
