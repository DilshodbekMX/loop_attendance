from django.contrib import admin
from .models import Csv, School, Teacher, Student, Attendance, SchoolClass
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.

admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Csv)



class AttendanceProfileAdmin(admin.ModelAdmin):
    list_display = ['student','teacher','date','mark_attendance']
admin.site.register(Attendance, AttendanceProfileAdmin)


class StudentAdmin(ImportExportModelAdmin):
    list_display = ("id", 'student_name', 'student_class', "student_teacher", 'student_school', 'student_gender') 
admin.site.register(Student,StudentAdmin)

class ClassAdmin(ImportExportModelAdmin):
    list_display = ('id', 'class_type', 'class_teacher', 'class_school', 'slug')
admin.site.register(SchoolClass,ClassAdmin)
