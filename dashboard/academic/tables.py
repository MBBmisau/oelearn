from academic.models import Batch
import django_tables2 as tables
from main.tables import MainTable


class BatchTable(MainTable):
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/academic/batch_row_edit.html', orderable=False)
    delete = tables.TemplateColumn(verbose_name='Delete', template_name='tables/dashboard/academic/batch_row_delete.html', orderable=False)

    table_title = 'List of all academic batch'
    icon = 'fas fa-graduation-cap'

    class Meta(MainTable.Meta):
        model = Batch
        fields = ('name', 'order',)
        sequence = ('name', 'order', 'edit', 'delete')
