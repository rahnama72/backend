from django.db import models


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


