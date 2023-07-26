import django_tables2 as tables
from main.tables import MainTable

from course.models import Subject

class SubjectTable(MainTable):
    #sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/course/subject_row_edit.html', orderable=False)
    delete = tables.TemplateColumn(verbose_name='Delete', template_name='tables/dashboard/course/subject_row_delete.html', orderable=False)

    table_title = 'List of all subjecs'
    icon = 'fas fa-bars'

    class Meta(MainTable.Meta):
        model = Subject
        fields = ('title', 'short_title',)
        sequence = ('title', 'short_title', 'edit', 'delete')
