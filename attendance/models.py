
from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from django.template.defaultfilters import slugify


schools_choice = [
    ('1-maktab','1-maktab'), ('2-maktab','2-maktab'), ('3-maktab','3-maktab'),('4-maktab','4-maktab'),('5-maktab','5-maktab'),('6-maktab','6-maktab'),
    ('7-maktab','7-maktab'), ('8-maktab','8-maktab'), ('9-maktab','9-maktab'), ('10-maktab','10-maktab'), ('11-maktab','11-maktab'),('12-maktab','12-maktab'),
    ('13-maktab','13-maktab'), ('14-maktab','14-maktab'),('15-maktab','15-maktab'), ('16-maktab','16-maktab'), ('17-maktab','17-maktab'),('18-maktab','18-maktab'),
    ('19-maktab','19-maktab'), ('20-maktab','22-maktab'),('23-maktab','23-maktab'),('24-maktab','24-maktab'), ('25-maktab','25-maktab'),('26-maktab','26-maktab'),
    ('33-maktab','33-maktab'),
]

class_list = [
    ('1-A sinf', '1-A sinf'), ('1-B sinf', '1-B sinf'), ('1-C sinf', '1-C sinf'), ('1-D sinf', '1-D sinf'), ('1-E sinf', '1-E sinf'),
    ('2-A sinf', '2-A sinf'), ('2-B sinf', '2-B sinf'), ('2-C sinf', '2-C sinf'), ('2-D sinf', '2-D sinf'), ('2-E sinf', '2-E sinf'),
    ('3-A sinf', '3-A sinf'), ('3-B sinf', '3-B sinf'), ('3-C sinf', '3-C sinf'), ('3-D sinf', '3-D sinf'), ('3-E sinf', '3-E sinf'),
    ('4-A sinf', '4-A sinf'), ('4-B sinf', '4-B sinf'), ('4-C sinf', '4-C sinf'), ('4-D sinf', '4-D sinf'), ('4-E sinf', '4-E sinf'),
    ('5-A sinf', '5-A sinf'), ('5-B sinf', '5-B sinf'), ('5-C sinf', '5-C sinf'), ('5-D sinf', '5-D sinf'), ('5-E sinf', '5-E sinf'),
    ('6-A sinf', '6-A sinf'), ('6-B sinf', '6-B sinf'), ('6-C sinf', '6-C sinf'), ('6-D sinf', '6-D sinf'), ('6-E sinf', '6-E sinf'),
    ('7-A sinf', '7-A sinf'), ('7-B sinf', '7-B sinf'), ('7-C sinf', '7-C sinf'), ('7-D sinf', '7-D sinf'), ('7-E sinf', '7-E sinf'),
    ('8-A sinf', '8-A sinf'), ('8-B sinf', '8-B sinf'), ('8-C sinf', '8-C sinf'), ('8-D sinf', '8-D sinf'), ('8-E sinf', '8-E sinf'),
    ('9-A sinf', '9-A sinf'), ('9-B sinf', '9-B sinf'), ('9-C sinf', '9-C sinf'), ('9-D sinf', '9-D sinf'), ('9-E sinf', '9-E sinf'),
    ('10-A sinf', '10-A sinf'), ('10-B sinf', '10-B sinf'), ('10-C sinf', '10-C sinf'), ('10-D sinf', '10-D sinf'), ('10-E sinf', '10-E sinf'),
    ('11-A sinf', '11-A sinf'), ('11-B sinf', '11-B sinf'), ('11-C sinf', '11-C sinf'), ('11-D sinf', '11-D sinf'), ('11-E sinf', '11-E sinf'),
]


gender_list = [("M", "M"), ("F", "F")]

class_attendance = (
    ('Bor','Bor'),
    ("Yo'q","Yo'q"),
    ('Sababli','Sababli'),
)

class School(models.Model):
    school_name = models.CharField(max_length=20, choices=schools_choice, default='1-maktab', unique=True, verbose_name="Maktab nomi")
    situated_district = models.CharField(max_length=30, default="Rishton", verbose_name="Maktab joylashgan tuman")
    situated_region = models.CharField(max_length=30, default="Farg'ona", verbose_name="Maktab joylashgan viloyat")
    timestamp = models.DateTimeField(auto_now_add=True)

    principal = models.OneToOneField(User, on_delete=models.CASCADE, related_name="school_principal")

    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.school_name

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.school_name} {self.situated_district}")
        super().save(*args, **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacheruser')
    
    first_name =  models.CharField(max_length=20, verbose_name='Ismi')
    last_name =  models.CharField(max_length=20, verbose_name='Familiyasi')
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Otasining ismi')
    phone = models.CharField(max_length=15, help_text="+99801112233", unique=True, verbose_name='Telefon raqami')
    work_place = models.CharField(max_length=20, choices=schools_choice, default='1-maktab', unique=True, verbose_name="Maktab nomi")
    user_status = models.CharField(max_length=100, verbose_name='Lavozimi')
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def get_absolute_url(self):
        return reverse("attendance:profile", kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.first_name}"

class SchoolClass(models.Model):
    class_type = models.CharField(max_length=20, choices=class_list, verbose_name='Sinf turi')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_class', verbose_name="O'qituvchi")
    class_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_class', verbose_name='Maktabi')
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.class_type} {self.class_school}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_type} {self.class_school}"


class Student(models.Model):
    student_name =  models.CharField(max_length=100, verbose_name="O'quvchi FISH")
    student_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='class_student', verbose_name='Sinfi')
    student_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_student', verbose_name="O'qituvchi")
    student_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_student', verbose_name='Maktabi')
    student_gender = models.CharField(choices=gender_list, max_length=10, verbose_name='Jinsi')
    present = models.IntegerField(default=0, verbose_name='Bor')
    cause = models.IntegerField(default=0, verbose_name='Sababli')
    absent = models.IntegerField(default=0, verbose_name="Yo'q")
    total = models.FloatField(verbose_name='Umumiy reyting (%)', blank=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} {self.student_class}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.student_name}")
        s = (self.present + self.absent + self.cause)
        if s > 0:
            self.total = (100 * self.present)/ s
        else:
            self.total = 0
        super().save(*args, **kwargs)
        
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    mark_attendance = models.CharField(max_length=50, choices=class_attendance)

    def __str__(self):
        return f"{self.student.student_name} {self.student.student_class} {self.student.student_school}"


class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs/')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
 
    def __str__(self):
        return f"File id: {self.id}"