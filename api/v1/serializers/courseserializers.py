from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    course = serializers.StringRelatedField(read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
            'students',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    # groups = GroupSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        groups = obj.groups.annotate(num_stud=Count('students'))
        students_count = 0
        for group in groups:
            students_count += group.num_stud
        return students_count

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп."""
        avg_groups = obj.groups.annotate(
            num_stud=Count('students')
        ).aggregate(avg=Avg('num_stud'))
        if avg_groups['avg']:
            return int(avg_groups['avg'] / obj.max_group_num * 100)
        return 0

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        subscriptions_count = Subscription.objects.filter(course=obj).count()
        users_count = User.objects.all().count()
        return int(subscriptions_count / users_count * 100)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            # 'min_group_num',
            # 'max_group_num',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
            # 'groups',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'min_group_num',
            'max_group_num',
        )
