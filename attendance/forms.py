from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Csv, School, SchoolClass, Teacher, Student, Attendance
from loop_attendance import settings

schools_choice = [
    ('1-maktab','1-maktab'), ('2-IDUM', '2-IDUM'),('2-maktab','2-maktab'), ('3-maktab','3-maktab'),('4-maktab','4-maktab'),('4-IDUM', '4-IDUM'),('5-maktab','5-maktab'),('6-maktab','6-maktab'),
    ('7-maktab','7-maktab'), ('8-maktab','8-maktab'), ('9-maktab','9-maktab'), ('10-maktab','10-maktab'), ('11-maktab','11-maktab'),('12-maktab','12-maktab'),
    ('13-maktab','13-maktab'), ('14-maktab','14-maktab'),('15-maktab','15-maktab'), ('16-maktab','16-maktab'), ('17-maktab','17-maktab'),('18-maktab','18-maktab'),
    ('19-maktab','19-maktab'), ('20-maktab','22-maktab'),('23-maktab','23-maktab'),('24-maktab','24-maktab'), ('25-maktab','25-maktab'),('26-maktab','26-maktab'),
    ('27-maktab','27-maktab'),('28-maktab','28-maktab'), ('29-maktab','29-maktab'), ('30-maktab','30-maktab'), ('31-maktab','31-maktab'),('32-maktab','32-maktab'),
    ('33-maktab','33-maktab'), ('34-maktab','34-maktab'),('35-maktab','35-maktab'), ('36-maktab','36-maktab'), ('37-maktab','37-maktab'),('38-maktab','38-maktab'),
    ('39-maktab','39-maktab'), ('40-maktab','40-maktab'), ('41-maktab','41-maktab'), ('42-maktab','42-maktab'), ('43-maktab','43-maktab'), 
    ('44-maktab','44-maktab'),('45-maktab','45-maktab'), ('46-maktab','46-maktab'), ('47-maktab','47-maktab'),('48-maktab','48-maktab'),
    ('49-maktab','49-maktab'), ('50-maktab','50-maktab'), ('51-maktab','51-maktab'), ('52-maktab','52-maktab'), ('53-maktab','53-maktab'),
    ('54-maktab','54-maktab'),('55-maktab','55-maktab'), ('56-maktab','56-maktab'), ('57-maktab','57-maktab'),('58-maktab','58-maktab'),
    ('59-maktab','59-maktab'), ('60-maktab','60-maktab'), ('61-maktab','61-maktab'), ('62-maktab','62-maktab'),('63-maktab','63-maktab'),
    ('64-maktab','64-maktab'),('65-maktab','65-maktab'), ('66-maktab','66-maktab'), ('67-maktab','67-maktab'),]
class_attendance = (
    ('Bor','Bor'),
    ("Yo'q","Yo'q"),
    ('Sababli','Sababli'),

)
class_list = [
    ('1-A sinf', '1-A sinf'), ('1-B sinf', '1-B sinf'),  ('1-D sinf', '1-D sinf'), ('1-E sinf', '1-E sinf'),('1-F sinf', '1-F sinf'),
    ('2-A sinf', '2-A sinf'), ('2-B sinf', '2-B sinf'),  ('2-D sinf', '2-D sinf'), ('2-E sinf', '2-E sinf'),('2-F sinf', '2-F sinf'),
    ('3-A sinf', '3-A sinf'), ('3-B sinf', '3-B sinf'), ('3-D sinf', '3-D sinf'), ('3-E sinf', '3-E sinf'),('3-F sinf', '3-F sinf'),
    ('4-A sinf', '4-A sinf'), ('4-B sinf', '4-B sinf'),  ('4-D sinf', '4-D sinf'), ('4-E sinf', '4-E sinf'),('4-F sinf', '4-F sinf'),
    ('5-A sinf', '5-A sinf'), ('5-B sinf', '5-B sinf'), ('5-D sinf', '5-D sinf'), ('5-E sinf', '5-E sinf'),('5-F sinf', '5-F sinf'),
    ('6-A sinf', '6-A sinf'), ('6-B sinf', '6-B sinf'), ('6-D sinf', '6-D sinf'), ('6-E sinf', '6-E sinf'),('6-F sinf', '6-F sinf'),
    ('7-A sinf', '7-A sinf'), ('7-B sinf', '7-B sinf'),  ('7-D sinf', '7-D sinf'), ('7-E sinf', '7-E sinf'),('7-F sinf', '7-F sinf'),
    ('8-A sinf', '8-A sinf'), ('8-B sinf', '8-B sinf'),  ('8-D sinf', '8-D sinf'), ('8-E sinf', '8-E sinf'),('8-F sinf', '8-F sinf'),
    ('9-A sinf', '9-A sinf'), ('9-B sinf', '9-B sinf'), ('9-D sinf', '9-D sinf'), ('9-E sinf', '9-E sinf'),('9-F sinf', '9-F sinf'),
    ('10-A sinf', '10-A sinf'), ('10-B sinf', '10-B sinf'), ('10-D sinf', '10-D sinf'), ('10-E sinf', '10-E sinf'),('10-F sinf', '10-F sinf'),
    ('11-A sinf', '11-A sinf'), ('11-B sinf', '11-B sinf'), ('11-D sinf', '11-D sinf'), ('11-E sinf', '11-E sinf'),('11-F sinf', '11-F sinf'),
]


gender_list = [("Erkak", "Erkak"), ("Ayol", "Ayol")]
class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    class Meta:
        model = User
        fields = ['username','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SchoolForm(forms.ModelForm):
    school_name = forms.ChoiceField(required=True, choices=schools_choice)
    class Meta:
        model = School
        fields = '__all__'  
        exclude = ('timestamp', 'principal', 'slug')

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Ismi')
    last_name = forms.CharField(required=True, label='Familiyasi')
    middle_name = forms.CharField(required=False, label='Otasining ismi')
    phone = forms.CharField(required=True, label='Telefon raqami')
    user_status = forms.CharField(required=True, label='Lavozimi')
    work_place = forms.ChoiceField(required=True, choices=schools_choice, label='Ishlaydigan maktabi')
    
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name','middle_name', 'phone','user_status', 'work_place')

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TeacherUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Ismi')
    last_name = forms.CharField(required=True, label='Familiyasi')
    middle_name = forms.CharField(required=False, label='Otasining ismi')
    phone = forms.CharField(required=True, label='Telefon raqami')
    user_status = forms.CharField(required=True, label='Lavozimi')
    work_place = forms.ChoiceField(required=True, choices=schools_choice, label='Ishlaydigan maktabi', disabled=True)
    
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name','middle_name', 'phone','user_status', 'work_place')

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ClassForm(forms.ModelForm):


    class Meta:
        model = SchoolClass
        fields = '__all__'
        exclude = ('class_teacher', 'class_school', 'slug')
    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('student_class', 'student_teacher', 'student_school', 'present', 'cause','absent', 'total', 'slug')
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AttendanceForm(forms.Form):
    mark_attendance = forms.ChoiceField(widget=forms.RadioSelect(), choices=class_attendance)

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)