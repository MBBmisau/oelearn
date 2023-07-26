from os import access
import django_tables2 as tables
from main.tables import MainTable

from certificate.models import Certificate
        
class CourseCerficateTable(MainTable):
    student = tables.Column(accessor='result__student')
    email = tables.Column(accessor='result__student__user__email')
    is_bound = tables.Column(accessor='bound_text', orderable=False)
    total_score = tables.Column(verbose_name='Total score', accessor='result__total_score', orderable=False)
    
    table_title = 'List of course certificates'
    icon = "fas fa-certificate"
    
    class Meta(MainTable.Meta):
        model = Certificate
        template_name = "tables/main_table.html"
        fields = ()
        sequence = ('student', 'email', 'total_score', 'is_bound')