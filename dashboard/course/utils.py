from course.models import Video

def has_live_video(module):
    for content in module.contents.filter(live=True):
        if type(content.item) == Video:
            return True
    return False