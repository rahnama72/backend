from django.db import models
from UserManager import models as UserMangerModels
from mptt.models import MPTTModel, TreeForeignKey
from Blog import fucntions as BlogFunctions


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
