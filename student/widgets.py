from django.forms import DateTimeInput
#from django.utils.safestring import mark_safe

class DatePickerInput(DateTimeInput):
    template_name = 'widgets/datepicker.html'
    
    def get_context(self, name, value, attrs):
        datepicker_id = 'datepicker_{name}'.format (name=name)
        if attrs is None:
            attrs = dict()
        attrs['data_target'] = '#{id}'.format(id='id1')
        attrs['class'] = 'form-control datatimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datepicker_id'] = 'id1'
        return context
  #  def render(self, name, value, attrs=None, renderer=None):
   #     html = super().render(name, value, attrs)
    #    inline_code = mark_safe(
     #       "<script>$(function () {$('#id1').datetimepicker({format: 'L',});});</script>"
      #  )
       # return html + inline_code
    class Media:
        css = {
            'all': ('plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css',)
        }
        js = ('plugins/moment/moment.min.js', 'plugins/tempusdominus-bootstrap-4/js/tempusdominus-bootstrap-4.min.js', 'js/datepicker.js')
       