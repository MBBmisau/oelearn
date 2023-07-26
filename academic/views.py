from django.shortcuts import render
from django.views.generic.base import TemplateView

class GraduateBatchStudent:
    """
    Exams must be finished
    Batch.is_current will be False
    """
    pass

class SetCurrentBatch:
    """
    There must not have any current batch
    """
    pass

class PortalClosed(TemplateView):
    template_name = 'academic/portal_closed.html'
