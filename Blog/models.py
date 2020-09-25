from django.db import models
from UserManager import models as UserMangerModels
from mptt.models import MPTTModel, TreeForeignKey
from Blog import fucntions as BlogFunctions
from Blog import variables as BlogVariables


# Create your models here.
class Category(UserMangerModels.BasicModel, MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children',
                            db_index=True, verbose_name='دسته بندی پدر')

    title = models.CharField(max_length=250, verbose_name='عنوان')
    content = models.TextField(max_length=500, verbose_name='متن')
    index_pic = models.ImageField(null=True, blank=True, upload_to='category-pics/', verbose_name='تصویر شاخص')
    slug = models.SlugField(unique=True, null=True, allow_unicode=True, verbose_name='آدرس اینترنتی(Slug)')

    class Meta:
        verbose_name_plural = 'دسته بندی های مطالب'
        verbose_name = 'دسته بندی مطالب'

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = BlogFunctions.slug_generator(self)
        super(Category, self).save(*args, **kwargs)


class Post(UserMangerModels.BasicModel):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='posts', verbose_name='دسته بندی')

    title = models.CharField(max_length=250, blank=False, verbose_name='عنوان')
    content = models.TextField(null=True, blank=True, verbose_name='متن')

    index_pic = models.ImageField(null=True, blank=True, upload_to='posts-pics/', verbose_name='تصویر شاخص')
    index_pic_alt_tag = models.CharField(max_length=100, verbose_name='متن جانشین عکس', null=True, blank=True, )
    publish_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انتشار')
    publish_time = models.TimeField(null=True, blank=True, verbose_name='زمان انتشار')
    status = models.IntegerField(choices=BlogVariables.POST_STATUS_CHOICES, default=BlogVariables.POST_STATUS_CHOICES[2][0],
                                 verbose_name='وضعیت')
    is_allow_comments = models.BooleanField(default=True, verbose_name='آیا کامنت بپذیرد؟')
    tags = models.CharField(max_length=250, null=True, blank=True, verbose_name='تگ ها')
    slug = models.SlugField(unique=True, null=True, allow_unicode=True, verbose_name='آدرس اینترنتی(Slug)')

    class Meta:
        verbose_name_plural = 'مطالب'
        verbose_name = 'مطلب'

    def __str__(self):
        return self.title

    @property
    def is_publish(self):
        if self.status == 3:
            if BlogFunctions.is_datetime_pass(date=self.publish_date, time=self.publish_time) is True:
                return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = BlogFunctions.slug_generator(self)
        super(Post, self).save(*args, **kwargs)


class Video(UserMangerModels.BasicModel):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='videos', verbose_name='دسته بندی')

    title = models.CharField(max_length=250, blank=False, verbose_name='عنوان')
    content = models.TextField(null=True, blank=True, verbose_name='متن')
    file = models.FileField(upload_to='videos/', null=True, verbose_name="فایل")

    publish_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انتشار')
    publish_time = models.TimeField(null=True, blank=True, verbose_name='زمان انتشار')
    status = models.IntegerField(choices=BlogVariables.POST_STATUS_CHOICES, default=BlogVariables.POST_STATUS_CHOICES[2][0],
                                 verbose_name='وضعیت')
    is_allow_comments = models.BooleanField(default=True, verbose_name='آیا کامنت بپذیرد؟')
    tags = models.CharField(max_length=250, null=True, blank=True, verbose_name='تگ ها')
    slug = models.SlugField(unique=True, null=True, allow_unicode=True, verbose_name='آدرس اینترنتی(Slug)')

    class Meta:
        verbose_name_plural = 'ویدئو ها'
        verbose_name = 'ویدئو'

    def __str__(self):
        return self.title

    @property
    def is_publish(self):
        if self.status == 3:
            if BlogFunctions.is_datetime_pass(date=self.publish_date, time=self.publish_time) is True:
                return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = BlogFunctions.slug_generator(self)
        super(Video, self).save(*args, **kwargs)
