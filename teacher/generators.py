import random
from django.utils import timezone

def generate_staff_id(first_name):

    def get_first_letter(name):
        word = name.strip()
        container = []
        for w in word:
            container.append(w)
        context = container[0].upper()
        return context

    rand_number = random.randint(1000, 9999)
    first_later = get_first_letter(first_name)
    return f'{first_later}{rand_number}'
