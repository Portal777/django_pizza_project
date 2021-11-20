from django.db import models
from django.conf import settings

# Create your models here.


class Topping(models.Model):
    title = models.CharField(max_length=30, verbose_name='название')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='описание')

    def __str__(self):
        return self.title

    def is_valid_topping(self):
        return self.title!=''


class Pizza(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='автор', null=True)
    title = models.CharField(max_length=30, verbose_name='название')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='описание')
    recipe = models.ManyToManyField(Topping, verbose_name='ингредиенты')
    slug = models.SlugField(max_length=50, verbose_name='ЧПУ', unique=True, null=True)
    image = models.ImageField(upload_to='pizza_image/%Y/%m/%d/', null=True)

    def __str__(self):
        return self.title

    def is_valid_pizza(self):
        return self.author!='' and self.title!='' and self.recipe!=None and self.slug!=''

    def return_recipe(self):
        return self.recipe
