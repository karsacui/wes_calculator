from django.db import models
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_wes_gpa(self):
        queryset = Course.objects.filter(student=self)
        gp_sum = 0
        credit_sum = 0
        test = ''
        for course in queryset:
            credit = course.get_wes_credit()
            gp_sum += course.get_wes_gp()*credit
            credit_sum += credit
            test += str(credit) + "*" + str(course.get_wes_gp()) + "+"
        print(test)
        print(gp_sum)
        print(credit_sum)
        return gp_sum / credit_sum

    def get_njupt_gpa(self):
        queryset = Course.objects.filter(student=self)
        gp_sum = 0
        credit_sum = 0
        for course in queryset:
            if course.type == 'RX':
                continue
            gp_sum += course.get_njupt_gp()*course.credit
            credit_sum += course.credit
        return gp_sum / credit_sum


class Course(models.Model):
    def __str__(self):
        if self.grade:
            return str(self.student)+self.name+self.grade
        else:
            return str(self.student)+self.name+str(self.score)

    class CourseType(models.TextChoices):
        BIXIU = 'BX', _('必修')
        XIANXUAN = 'XX', _('限选')
        RENXUAN = 'RX', _('任选')

    class Grade(models.TextChoices):
        A = 'A', _('优秀')
        B = 'B', _('良好')
        C = 'C', _('中等')
        D = 'D', _('及格')
        F = 'F', _('不及格')
        PASS = 'P', _('通过')

    course_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=2, choices=CourseType.choices, default=CourseType.BIXIU)
    credit = models.FloatField()
    override_credit = models.FloatField(null=True, blank=True)
    semester = models.IntegerField()
    score = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=1, choices=Grade.choices, default='', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)

    def get_wes_credit(self):
        if self.override_credit == None:
            return self.credit
        else:
            return self.override_credit

    def get_njupt_gp(self):
        grade_gp_dict = {
            'A': 4.5,
            'B': 3.5,
            'C': 2.5,
            'D': 1.5,
            'F': 0,
            'P': 1.1,
        }
        if self.grade in grade_gp_dict.keys():
            return grade_gp_dict[self.grade]
        else:
            if self.score >= 60:
                return self.score * 0.1 - 5
            else:
                return 0

    def get_wes_gp(self):
        grade_gp_dict = {
            'A': 4,
            'B': 3,
            'C': 2,
            'D': 1,
            'F': 0,
            'P': 2,
        }
        if self.grade in grade_gp_dict.keys():
            return grade_gp_dict[self.grade]
        else:
            if self.score >= 85:
                return 4
            elif self.score >= 75:
                return 3
            elif self.score >= 60:
                return 2
            else:
                return 1

