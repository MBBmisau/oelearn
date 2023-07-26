from django.contrib.auth import get_user_model

UserModel = get_user_model()

def get_user(reg_id):
    try:
        user = UserModel.objects.get(reg_id=reg_id)
    except:
        user = None
    return user
