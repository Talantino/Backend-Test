from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Group


class CustomerUser(AbstractUser):
    """
    A customed user model of the STUDENT
    """
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        related_name='students',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Subscription(models.Model):
    """"
    Model for subscribing
    """
    student = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Студент'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course',
            )
        ]

    def __str__(self):
        return f'{self.student} подписан на курс {self.course}'
