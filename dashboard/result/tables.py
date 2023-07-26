import django_tables2 as tables
from main.tables import MainTable
from result.models import StudentCA, StudentExam, Grade
        
class StudentCATable(MainTable):
    #sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    max_score = tables.Column(accessor='max_possible_score')
    mark = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/result/student_ca_row_mark.html', orderable=False)
    
    table_title = 'List of subjecs'
    icon = "fas fa-compass"
    
    class Meta(MainTable.Meta):
        model = StudentCA
        template_name = "tables/main_table.html"
        fields = ('student', 'score', 'marked')
        sequence = ('student', 'score', 'max_score', 'marked', 'mark')

class StudentExamTable(MainTable):
    #sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    max_score = tables.Column(accessor='max_possible_score')
    mark = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/result/student_exam_row_mark.html', orderable=False)
    
    table_title = 'List of subjecs'
    icon = "fas fa-compass"
    
    class Meta(MainTable.Meta):
        model = StudentExam
        template_name = "tables/main_table.html"
        fields = ('student', 'score', 'marked')
        sequence = ('student', 'score', 'max_score', 'marked', 'mark')

class GradeTable(MainTable):
    #sn = tables.TemplateColumn('{{ row_counter }}', verbose_name='S/N', orderable=False)
    edit = tables.TemplateColumn(verbose_name='Edit', template_name='tables/dashboard/result/grade_row_edit.html', orderable=False)
    delete = tables.TemplateColumn(verbose_name='Delete', template_name='tables/dashboard/result/grade_row_delete.html', orderable=False)

    table_title = 'List of all grades'
    icon = 'fas fa-align-justify'

    class Meta(MainTable.Meta):
        model = Grade
        template_name = "tables/main_table.html"
        fields = ('name', 'start_score', 'end_score', 'remark')
        sequence = ('name', 'start_score', 'end_score', 'remark', 'edit', 'delete')
