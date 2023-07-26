import random
from django.utils import timezone

from academic.utils import get_current_batch
from .utils import sanitizer

BATCH = get_current_batch()

def generate_admission_no(first_name):

    def get_first_letter(name):
        word = name.strip()
        container = []
        for w in word:
            container.append(w)
        context = container[0].upper()
        return context

    rand_number = random.randint(1000, 9999)
    current_year = timezone.now().year
    first_later = get_first_letter(first_name)
    return f'{current_year}/{first_later}{rand_number}'

def generate_admission_no_orl(student):
    #AH/01/001
    def get_batch():
        if student.start_batch:
            return student.start_batch
        return BATCH
    ah_prefix = 'AH'
    batch = get_batch()
    batch_id = sanitizer(batch.id, 2)
    student_id = sanitizer(student.id, 3)
    return f'{ah_prefix}/{batch_id}/{student_id}'