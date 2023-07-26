import django_tables2 as tables

from main.tables import MainTable

from student.models import Student

class StudentTable(MainTable):
    reg_number = tables.Column(verbose_name='Reg. Number', accessor='user.reg_id')
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/student/student_row_edit.html', orderable=False)
    detail = tables.TemplateColumn(verbose_name='Detail', template_name='tables/dashboard/student/student_row_view.html', orderable=False)

    table_title = 'List of all teachers'
    icon = 'fas fa-user-shield'

    class Meta(MainTable.Meta):
        model = Student
        fields = ('user.first_name', 'user.email', 'user.is_active',)
        sequence = ('user.first_name', 'user.email', 'reg_number', 'user.is_active', 'detail', 'edit',)





















































































































































