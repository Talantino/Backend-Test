from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    creator = models.CharField(verbose_name="Автор", max_length=255)
    name = models.CharField(verbose_name="Название Продукта", max_length=255)
    start_date = models.DateTimeField(verbose_name="Дата и время старта", auto_now_add=True)
    price = models.DecimalField(verbose_name="Стоимость", max_digits=10, decimal_places=2)
    min_group_users = models.PositiveIntegerField()
    max_group_users = models.PositiveIntegerField()

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} by {self.creator}"


class Student(models.Model):
    # first_name = models.CharField(verbose_name="Имя Студента", max_length=255)
    # last_name = models.CharField(verbose_name="Фамилия Студента", max_length=255)
    # email = models.EmailField(unique=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='StudentProductAccess')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f"{self.user.username}'s Student Profile"


class Lesson(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название Урока", max_length=255)
    video_link = models.URLField()

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f"Lesson: {self.name} Product: {self.product}"


class Group(models.Model):
    students = models.ManyToManyField("Student")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    group_name = models.CharField(verbose_name="Название Группы", max_length=255)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f"В группу {self.group_name} входят: {self.students}"


class StudentProductAccess(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Доступы студентов"

    def __str__(self):
        return f"{self.student} имеет доступ к {self.product}"
