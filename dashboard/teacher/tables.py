import django_tables2 as tables

from main.tables import MainTable

from teacher.models import Teacher

class TeachersTable(MainTable):
    #sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    staff_id = tables.Column(verbose_name='Staff ID', accessor='user.reg_id')
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/teacher/teacher_row_edit.html', orderable=False)
    detail = tables.TemplateColumn(verbose_name='Detail', template_name='tables/dashboard/teacher/teacher_row_view.html', orderable=False)
    #passport = tables.TemplateColumn(verbose_name='Passport', template_name='tables/student/student_row_image.html', orderable=False)

    table_title = 'List of all teachers'
    icon = 'fas fa-user-shield'

    class Meta(MainTable.Meta):
        model = Teacher
        fields = ('user.first_name', 'user.email', 'user.is_active', 'user.is_admin',)
        sequence = ('user.first_name', 'user.email', 'staff_id', 'user.is_active', 'user.is_admin', 'detail', 'edit',)
