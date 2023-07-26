import django_tables2 as tables
from main.tables import MainTable
from result.models import StudentCA, StudentExam, Grade
        
class StudentCATable(MainTable):
    max_score = tables.Column(accessor='max_possible_score')
    
    table_title = 'All assessments'
    icon = "fas fa-compass"
    
    class Meta(MainTable.Meta):
        model = StudentCA
        template_name = "tables/main_table.html"
        fields = ('student', 'ca', 'module', 'score')
        sequence = ('student', 'ca', 'module', 'score', 'max_score')

class StudentExamTable(MainTable):
    max_score = tables.Column(accessor='max_possible_score')
    
    table_title = 'All examinations'
    icon = "fas fa-compass"
    
    class Meta(MainTable.Meta):
        model = StudentExam
        template_name = "tables/main_table.html"
        fields = ('student', 'exam', 'score')
        sequence = ('student', 'exam', 'score', 'max_score')