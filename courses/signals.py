from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from courses.models import Group
from users.models import CustomUser, Subscription


def redistribution(course):
    """Перераспределение студентов по группам примерно поровну."""

    subscriptions = Subscription.objects.filter(
        course=course
    ).prefetch_related('student')
    students_for_update = []
    for subscription in subscriptions:
        students_for_update.append(subscription.student)
    subscriptions_count = subscriptions.count()
    groups_in_course = course.groups.all()
    groups_count = groups_in_course.count()
    mid_num = subscriptions_count // groups_count
    students_for_bulk_update = []
    for group in groups_in_course:
        for student in students_for_update[:mid_num]:
            student.group = group
            students_for_bulk_update.append(student)
        students_for_update = students_for_update[mid_num:]
    CustomUser.objects.bulk_update(students_for_bulk_update, ['group'])


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Запись нового студента в группу курса.

    Если количество групп в курсе равно нулю, создаем группу.
    Считаем количество студентов в существующих группах.
        Фильтруем группы, в которых количество студентов меньше максимально
        разрешенного и сортируем их по количеству студентов.
        Выбираем группу с наименьшим количеством, чтобы кол-во во всех группах
        не отличалось больше, чем на 1.
    Если курс уже начался, без фильтрации выбираем первую группу с наименьшим
    количеством студентов.
        Записываем студента в эту группу.
    Если все группы полные, создаем новую и перезаписывем студентов по группам
    примерно поровну.
    """

    if created:
        course = instance.course
        student = instance.student
        groups_count = course.groups.all().count()
        if groups_count == 0:
            group = Group.objects.create(
                course=course,
                title=f'Группа №{groups_count + 1}'
            )
        else:
            groups = course.groups.annotate(num_stud=Count('students'))
            if course.start_date >= timezone.now():
                group = groups.filter(
                    num_stud__lt=course.max_group_num
                ).order_by('num_stud').first()
            else:
                group = groups.order_by('num_stud').first()
        if group:
            student.group = group
            student.save()
        else:
            Group.objects.create(
                course=course,
                title=f'Группа №{groups_count + 1}'
            )
            redistribution(course)
