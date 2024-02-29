from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    creator = models.CharField(verbose_name="Автор", max_length=100)
    name = models.CharField(verbose_name="Название Продукта", max_length=100)
    start_date = models.DateTimeField(verbose_name="Дата и время старта")
    price = models.DecimalField(verbose_name="Стоимость", max_digits=10, decimal_places=2)
    min_group_users = models.PositiveIntegerField()
    max_group_users = models.PositiveIntegerField()

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name, self.start_date


class Student(models.Model):
    name = models.CharField(verbose_name="Имя Студента", max_length=100)
    products = models.ManyToManyField('Product', through='StudentProductAccess')


class Lesson(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название Урока", max_length=100)
    video_link = models.URLField()

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    students = models.ManyToManyField("Student")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    group_name = models.CharField(verbose_name="Название Группы", max_length=100)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = 'Группы'


class StudentProductAccess(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Доступы студентов"
