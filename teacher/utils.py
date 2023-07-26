from rolepermissions.roles import get_user_roles

from  set_class.models import SubjectCombination, StudentClass
from session_term.models import AcademicSession, AcademicTerm
from result.models import SubjectClearance

try:
    SESSION = AcademicSession.objects.get(is_current=True)
except:
    SESSION = None
try:
    TERM = AcademicTerm.objects.get(is_current=True)
except:
    TERM = None

def form_classes(teacher):
        try:
            classses = StudentClass.objects.filter(form_master=teacher)
            if len(classses) > 0:
                return classses
            else:
                return None
        except:
            return None


def is_form_master(teacher):
    return form_classes(teacher) is not None

def check_form_class(teacher, class_id):
    try:
        check = StudentClass.objects.get(id=class_id, form_master=teacher)
        return check
    except:
        return None

def has_form_class(teacher, class_id):
    return check_form_class(teacher=teacher, class_id=class_id) is not None

def subject_clear_list(student_class):
    combinations = SubjectCombination.objects.filter(term=TERM,student_class=student_class)
    clearance = SubjectClearance.objects.filter(term=TERM,session=SESSION,student_class=student_class,is_clear=True)
    clear_list = []
    for combination in combinations:
        for clr in clearance:
            if clr.subject == combination.subject:
                clear_list.append('clear')
                break
        else:
            clear_list.append('not_clear')
    return clear_list

def subject_clear_dict(student_class):
    combinations = SubjectCombination.objects.filter(term=TERM,student_class=student_class)
    clearance = SubjectClearance.objects.filter(term=TERM,session=SESSION,student_class=student_class,is_clear=True)
    clear_dict = {}
    for combination in combinations:
        for clr in clearance:
            if clr.subject == combination.subject:
                clear_dict[clr.subject.name] = 'clear'
                break
        else:
            clear_dict[combination.subject.name] = 'not_clear'
    return clear_dict

def clear_subjects(student_class):
    clearance = SubjectClearance.objects.filter(term=TERM,session=SESSION,student_class=student_class,is_clear=True)
    clear_list = []
    for clr in clearance:
        clear_list.append(clr.subject.name)

    return clear_list


def check_teacher(teacher, subject, student_class, term):
    try:
        combination = SubjectCombination.objects.get(teacher=teacher,subject=subject,student_class=student_class,term=term)
        return combination
    except:
        return None

def subject_classes(teacher):
    try:
        subj = SubjectCombination.objects.filter(teacher=teacher,term=TERM)
        if len(subj) > 0:
            return subj
        else:
            return None
    except:
        return None

def is_taking_class(teacher):
    return subject_classes(teacher) is not None

def is_role_user(user):
    roles = get_user_roles(user)
    return len(roles) > 0
