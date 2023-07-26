import django_tables2 as tables
from main.tables import MainTable
from .models import SocialLink
        
class SocialLinkTable(MainTable):
    sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/config/social_link_row_edit.html', orderable=False)
    delete = tables.TemplateColumn(verbose_name='Delete', template_name='tables/config/social_link_row_delete.html', orderable=False)
    
    table_title = 'List of social school media links'
    
    class Meta(MainTable.Meta):
        model = SocialLink
        template_name = "tables/main_table.html"
        fields = ('name', 'icon', 'url')
        sequence = ('sn', 'name', 'icon', 'url', 'edit', 'delete')