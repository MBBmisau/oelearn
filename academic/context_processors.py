from .utils import get_current_batch

def get_current_batch_to_context(request):
    return {
        'current_batch': get_current_batch(),
    }
