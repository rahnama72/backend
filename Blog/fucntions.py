from django.utils.text import slugify
from django.utils import timezone as tz

def slug_generator(instance, index=1, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title, allow_unicode=True)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{index}".format(slug=slug, index=index)
        return slug_generator(instance, index=index + 1, new_slug=new_slug)
    return slug


def get_localdate(init=None):
    return tz.localdate(init)


def get_localtime():
    return tz.localtime().time()


def datetime_compare(date_1, time_1, date_2, time_2):
    if date_1 > date_2:
        return False, 'd'
    elif date_1 == date_2 and time_1 > time_2:
        return False, 't'
    else:
        return True, ''


def is_datetime_pass(date, time):
    date_now = get_localdate()
    time_now = get_localtime()
    r, s = datetime_compare(
        date_1=date,
        time_1=time,
        date_2=date_now,
        time_2=time_now,
    )
    if r is True:
        return True
    else:
        return False