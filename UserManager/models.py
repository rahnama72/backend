from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager, UnicodeUsernameValidator


# Create your models here.
class BasicModel(models.Model):
    create_by = models.ForeignKey('User', default=1, on_delete=models.SET_DEFAULT,
                                  verbose_name='سازنده', related_name='create_%(class)ss')
    update_by = models.ForeignKey('User', default=1, on_delete=models.SET_DEFAULT,
                                  verbose_name='آخرین ویرایش کننده', related_name='update_%(class)ss')

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True
        ordering = ['create_date']


class User(AbstractBaseUser, BasicModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=120, unique=True, validators=[username_validator], verbose_name='نام کاربری')
    activation_code = models.CharField(max_length=120, blank=True, null=True, verbose_name='کد فعال سازی')
    first_name = models.CharField(verbose_name='نام', max_length=30)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=30)
    mobile = models.CharField(max_length=11, validators=[RegexValidator(r'^[0-9]{11}$')],
                              verbose_name='شماره همراه')
    email = models.EmailField(verbose_name='پست الکترونیکی')

    avatar = models.ImageField(upload_to='users', blank=True, null=True)

    is_active = models.BooleanField(verbose_name='وضعیت', default=True)
    is_verified = models.BooleanField(verbose_name='کد فعال سازی', default=False)
    is_staff = models.BooleanField(verbose_name='وضعیت کارمندی', default=False)
    is_superuser = models.BooleanField(verbose_name='ابر کاربر', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'email']

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

