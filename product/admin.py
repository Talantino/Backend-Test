from django.contrib import admin
from .models import Product, StudentProductAccess, Lesson, Group, Student
# Register your models here.

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(StudentProductAccess)
admin.site.register(Group)
admin.site.register(Student)
