from .models import Batch

def get_current_batch():
    try:
        batch = Batch.objects.get(is_current=True)
    except:
        batch = None
    return batch

def clear_batch_ref():
    #remove all students from courses
    pass
