import django_tables2 as tables

from main.tables import MainTable

from .models import Student
        
class StudentTable(MainTable):
    sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    admission_number = tables.Column(verbose_name='Admission number', accessor='user.reg_id')
    edit = tables.TemplateColumn(verbose_name='', template_name='tables/student/student_row_edit.html', orderable=False)
    detail = tables.TemplateColumn(verbose_name='Detail', template_name='tables/student/student_row_view.html', orderable=False)
    passport = tables.TemplateColumn(verbose_name='Passport', template_name='tables/student/student_row_image.html', orderable=False)
   # delete = tables.TemplateColumn(verbose_name='Delete', template_name='tables/set_class/set_row_delete.html', orderable=False)
    
    table_title = 'List of students in this class'
    
    class Meta:
        model = Student
        fields = ('user.first_name', 'user.last_name', 'user.middle_name', 'user.gender','is_suspended')
        sequence = ('sn', 'user.first_name', 'user.last_name', 'user.middle_name', 'admission_number', 'passport', 'user.gender', 'is_suspended', 'detail', 'edit',)
    