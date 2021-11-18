from django.contrib import admin

# Register your models here.
from .models import Student, Course


# admin.site.register(Student)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_wes_gpa', 'get_njupt_gpa', )


# admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'credit', 'get_wes_credit', 'get_wes_gp', 'pk',)
