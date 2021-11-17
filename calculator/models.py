from django.db import models
from django.db.models.query_utils import select_related_descend
from django.utils.translation import gettext_lazy as _

class Student(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_gpa(self):
        pass

class Course(models.Model):

    def __str__(self):
        pass

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

    def get_njupt_gp(self):
        if self.grade != '':
            grade_gp_dict = {
                'A': 4.5,
                'B': 3.5,
                'C': 2.5,
                'D': 1.5,
                'F': 0,
                'P': 1.1,
            }
            return grade_gp_dict[self.grade]
        else:
            if self.score >= 60:
                return self.score * 0.1 - 5
            else:
                return 0

    def get_wes_gp(self):
        if self.grade != '':
            grade_gp_dict = {
                'A': 4,
                'B': 3,
                'C': 2,
                'D': 1,
                'F': 0,
                'P': 2,
            }
            return grade_gp_dict[self.grade]
        else:
            