import csv
from zipfile import BadZipfile
import openpyxl
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Csv, Teacher, School, Student, Attendance, SchoolClass
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CsvModelForm, SchoolForm, UserForm, TeacherForm, AttendanceForm, StudentForm, TeacherUpdateForm, ClassForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.utils.timezone import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import timedelta, date, time
from django.utils import timezone


# ##############################
#                              # 
#     Administrator uchun      #
#                              # 
################################

class AdminDashboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'attendance/dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['teachers'] = Teacher.objects.all()
        context['students'] = Student.objects.all()
        context['attendance'] = Attendance.objects.all()
        context['date'] = datetime.today().date()
        special_date = datetime.today().date()

        if Attendance.objects.filter(date=datetime.today().date()).count() == 0  and timezone.now().date().weekday()==0:
            context['date'] = datetime.today().date() - timedelta(days=2)

        elif Attendance.objects.filter(date=datetime.today().date()).count() == 0  and timezone.now().date().weekday() > 0:
            context['date'] = datetime.today().date() - timedelta(days=1)
        # Total daily report
        context['total_present'] = Attendance.objects.filter(date=context['date'], mark_attendance='Bor' ).count()
        context['p_percent'] = round(((context['total_present'] * 100) / Student.objects.all().count()), 2)
        context['total_cause'] = Attendance.objects.filter(date=context['date'], mark_attendance='Sababli' ).count()
        context['c_percent'] = round(((context['total_cause'] * 100) / Student.objects.all().count()), 2)
        context['total_absent'] = Attendance.objects.filter(date=context['date'], mark_attendance="Yo'q" ).count()
        context['a_percent'] = round(((context['total_absent'] * 100) / Student.objects.all().count()), 2)
        context['wp_label'], context['wa_label'], context['wc_label'], context['date_label'] = [], [], [], []
        context['mp_label'], context['ma_label'], context['mc_label'], context['monthly_date_label'] = [], [], [], []
        context['is_sunday'] = False
        # Total weekly report
        for i in range(6,-1,-1):
            some_day_last_week = timezone.now().date() - timedelta(days=i)
            if some_day_last_week.weekday()!=6:
                context['date_label'].append(datetime.strftime(datetime.now()- timedelta(i), '%d/%m/%y'))
                present = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Bor' ).count()
                context['wp_label'].append(round(((present * 100) / Student.objects.all().count()), 2))
                cause = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Sababli' ).count()
                context['wc_label'].append(round(((cause * 100) / Student.objects.all().count()), 2))
                absent = Attendance.objects.filter(date=some_day_last_week, mark_attendance="Yo'q" ).count()
                context['wa_label'].append(round(((absent * 100) / Student.objects.all().count()), 2))
            elif timezone.now().date().weekday()==6:
                    context['is_sunday'] = True
        # Total monthly report
        for i in range(31,-1,-1):
            some_day_last_week = timezone.now().date() - timedelta(days=i)
            if some_day_last_week.weekday()!=6:
                context['monthly_date_label'].append(datetime.strftime(datetime.now()- timedelta(i), '%d/%m/%y'))
                present = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Bor' ).count()
                context['mp_label'].append(round(((present * 100) / Student.objects.all().count()), 2))
                cause = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Sababli' ).count()
                context['mc_label'].append(round(((cause * 100) / Student.objects.all().count()), 2))
                absent = Attendance.objects.filter(date=some_day_last_week, mark_attendance="Yo'q" ).count()
                context['ma_label'].append(round(((absent * 100) / Student.objects.all().count()), 2))     
            elif timezone.now().date().weekday() ==6:
                    context['is_sunday'] = True
                    
        context['wp_percent'] = round(sum(context['wp_label'])/len(context['wp_label']),2)
        context['mp_percent'] = round(sum(context['mp_label'])/len(context['mp_label']),2)
        context['wc_percent'] = round(sum(context['wc_label'])/len(context['wc_label']),2)
        context['mc_percent'] = round(sum(context['mc_label'])/len(context['mc_label']),2)
        context['wa_percent'] = round(sum(context['wa_label'])/len(context['wa_label']),2)
        context['ma_percent'] = round(sum(context['ma_label'])/len(context['ma_label']),2)
        school_context = {}
        s_name = []
        s_a_student = []
        s_t_p = []
        s_t_c = []
        s_t_a = []
        s_t_pp = []
        s_t_cp = []
        s_t_ap = []
        context['school_list'] = []
        for schoo in context['schools']:
            schools = get_object_or_404(School.objects.filter(school_name=schoo))
            school = School.objects.filter(school_name=schoo)
            s_name.append(schools)
            teacher = Teacher.objects.filter(work_place=schoo)
            if (Student.objects.filter(student_school__in=school).count()) >0:
                school_context['school_all_students'] = (Student.objects.filter(student_school__in=school).count())
                s_a_student.append(school_context['school_all_students'])
                school_all_students= (Student.objects.filter(student_school__in=school).count()) * (timezone.now().date().weekday() + 1)
                school_context['school_total_present'] = Attendance.objects.filter(date__week=special_date.isocalendar()[1], mark_attendance='Bor',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_p.append(school_context['school_total_present'])
                school_context['school_total_cause'] = Attendance.objects.filter(date__week=special_date.isocalendar()[1], mark_attendance='Sababli',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_c.append(school_context['school_total_cause'])
                school_context['school_total_absent'] = Attendance.objects.filter(date__week=special_date.isocalendar()[1], mark_attendance="Yo'q",teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_a.append(school_context['school_total_absent'])
                school_context['school_total_ppercent'] = round(school_context['school_total_present'] * 100 / school_all_students, 2)
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = round(school_context['school_total_cause'] * 100 / school_all_students, 2)
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = round(school_context['school_total_absent'] * 100 / school_all_students, 2)
                s_t_ap.append(school_context['school_total_apercent'])

            else:
                school_context['school_all_students'] = "O'quvchi kiritilmagan"
                s_t_p.append(0)
                s_t_c.append(0)
                s_t_a.append(0)
                s_a_student.append(school_context['school_all_students'])
                school_context['school_total_ppercent'] = 0
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = 0
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = 0
                s_t_ap.append(school_context['school_total_apercent'])
            
            context['school_list'] = zip(s_name, s_a_student, s_t_p, s_t_c, s_t_a, s_t_pp, s_t_cp, s_t_ap )

        return context

class AdminSchoolListView(LoginRequiredMixin, ListView):
    template_name = 'attendance/dashboard/school_list.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(AdminSchoolListView, self).get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['date'] = datetime.today().date()
        school_context = {}
        s_name = []
        s_a_student = []
        s_t_p = []
        s_t_c = []
        s_t_a = []
        s_t_pp = []
        s_t_cp = []
        s_t_ap = []
        s_a_s = []
        context['school_list'] = []
        for schoo in context['schools']:
            school = School.objects.filter(school_name=schoo)
            schools = get_object_or_404(School.objects.filter(school_name=schoo))
            school_attendance = Attendance.objects.filter(teacher__work_place=schoo, date=context["date"]).count()
            school_all_student = Student.objects.filter(student_school__in=school).count()
            s_name.append(schools)
            teacher = Teacher.objects.filter(work_place=schoo)
            if school_all_student >0:
                school_context['school_attendance_status'] = round((100 * school_attendance) / school_all_student,2)
                s_a_s.append(school_context['school_attendance_status'])
                school_context['school_all_students'] = (Student.objects.filter(student_school__in=school).count())
                s_a_student.append(school_context['school_all_students'])
                school_all_students= (Student.objects.filter(student_school__in=school).count()) * (timezone.now().date().weekday() + 1)
                school_context['school_total_present'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance='Bor',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_p.append(school_context['school_total_present'])
                school_context['school_total_cause'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance='Sababli',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_c.append(school_context['school_total_cause'])
                school_context['school_total_absent'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance="Yo'q",teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_a.append(school_context['school_total_absent'])
                school_context['school_total_ppercent'] = round(school_context['school_total_present'] * 100 / school_all_students, 2)
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = round(school_context['school_total_cause'] * 100 / school_all_students, 2)
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = round(school_context['school_total_absent'] * 100 / school_all_students, 2)
                s_t_ap.append(school_context['school_total_apercent'])

            else:
                school_context['school_all_students'] = "O'quvchi kiritilmagan"
                s_t_p.append(0)
                s_t_c.append(0)
                s_t_a.append(0)
                s_a_s.append(0)
                s_a_student.append(school_context['school_all_students'])
                school_context['school_total_ppercent'] = 0
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = 0
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = 0
                s_t_ap.append(school_context['school_total_apercent'])
            
            context['school_list'] = zip(s_name, s_a_student, s_t_p, s_t_pp, s_a_s)
        return context

@user_passes_test(lambda u: u.is_superuser)
def AdminXlsxFileAdd(request):
    if "GET" == request.method:
        return render(request, 'attendance/dashboard/add_xlsx_file.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        is_bad_zip = False
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet_list = [sheet.title for sheet in wb]
            for i in sheet_list:
                try:
                    worksheet = wb[i]
                    excel_data = list()
                    for row in range(1, 17):
                        row_data = list()
                        for cell in worksheet[row]:
                            row_data.append(str(cell.value))
                        excel_data.append(row_data)
                    for row in range(2, worksheet.max_row + 1):
                        full_name = (worksheet[f'B{row}'].value)
                        student_school = School.objects.get(school_name=(worksheet[f'D{row}'].value))
                        student_teacher = Teacher.objects.get(work_place=student_school)
                        student_class, created = SchoolClass.objects.get_or_create(
                                            class_type=(worksheet[f'C{row}'].value), 
                                            class_school=student_school, 
                                            class_teacher=student_teacher
                                    )
                        if ((full_name.split(' '))[0]).endswith("v"):
                            student_gender = 'M'
                        else:
                            student_gender = 'F'
                       
                        student_add, created = Student.objects.get_or_create(
                                    student_name = full_name,
                                    student_class = student_class,
                                    student_teacher = student_teacher,
                                    student_school = student_school,
                                    student_gender = student_gender,
                                )
                    break
                except KeyError:
                    excel_data = "Ma'lumot kiritishda xatolik"
        except BadZipfile:
            is_bad_zip = True
            excel_data = "XLSX fayl bo'lishi kerak"
        
            
        context = {"excel_data":excel_data, 'is_bad_zip':is_bad_zip}

        return render(request, 'attendance/dashboard/add_xlsx_file.html', context)

@user_passes_test(lambda u: u.is_superuser)
def AdminSchoolDetailView(request, pk):
    schools = get_object_or_404(School.objects.filter(pk=pk), )
    teacher = get_object_or_404(Teacher.objects.all(), work_place=schools.school_name)
    school = School.objects.filter(pk=pk)
    students=Student.objects.filter(student_school__in=school)
    school_class = SchoolClass.objects.filter(class_school__in=school)
    class_percent_list = []
    class_list = []

    for classes in school_class:
        student_percent_list = []
        
        classe = get_object_or_404(SchoolClass.objects.filter(slug=classes.slug))
        student_classes = SchoolClass.objects.filter(slug=classes.slug)
        studenta = Student.objects.filter(student_class__in=student_classes)
        for student in studenta:
            studente = get_object_or_404(Student.objects.filter(pk=student.pk, student_class=classes))
            present = studente.present
            cause = studente.cause
            absent = studente.absent
            if (present + absent + cause) > 0:
                student_percent = round((100 * present) / (present + absent + cause),2)
            else:
                student_percent = 0 
            student_percent_list.append(student_percent)
        if len(student_percent_list) > 0:    
            class_percent_list.append(round((sum(student_percent_list)/len(student_percent_list)),2))
        else: 
            class_percent_list.append(0)
        class_list.append(classe)
    about_class = zip(class_list, class_percent_list)
   
    context = {
        'schools':schools,
        'school_class':school_class,
        'students': students,
        'about_class':about_class,
    }
    return render(request,'attendance/dashboard/school_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def ClassDetailView(request, pk, slug):
    schools = get_object_or_404(School.objects.all(), pk=pk)
    school_class = get_object_or_404(SchoolClass.objects.filter(slug=slug))
    classes = SchoolClass.objects.filter(slug=slug)
    all_class = SchoolClass.objects.filter(class_school=schools)
    students = Student.objects.filter(student_class__in=classes)
    student_percent_list = []
    student_list = []

    for student in students:
        studente = get_object_or_404(Student.objects.filter(slug=student.slug))
        present = studente.present
        cause = studente.cause
        absent = studente.absent
        if (present + absent + cause) > 0:
            student_percent = round((100 * present) / (present + absent + cause),2)
        else:
            student_percent = 0 
        student_percent_list.append(student_percent)
        student_list.append(studente)
    about_student = zip(student_list, student_percent_list)
    
    if request.user.is_superuser:
        sc_form = StudentForm(request.POST or None)
        if request.method == 'POST':
            if 'student_create_btn' in request.POST:
                if sc_form.is_valid():
                    s_create = sc_form.save(commit=False)
                    s_create.student_class = school_class
                    s_create.student_teacher = schools.principal.teacheruser
                    s_create.student_school = schools
                    s_create.save()

            elif 'clas_delete_btn' in request.POST:
                obj = school_class
                obj.delete()
                return  redirect('attendance:admin_school_detail',pk=schools.pk)
            return  redirect('attendance:admin_class_detail',pk=schools.pk, slug=school_class.slug)

    context = {
        'schools':schools,
        'school_class':school_class,
        'classes':classes,
        'students': students,
        'sc_form':sc_form,

        'about_student':about_student,
    }

    return render(request,'attendance/dashboard/admin_class_detail.html', context)
    
@user_passes_test(lambda u: u.is_superuser)
def AdminStudentDetailView(request, pk, class_slug, student_slug):
    schools = get_object_or_404(School.objects.all(), pk=pk)
    school_class = get_object_or_404(SchoolClass.objects.filter(slug=class_slug))
    classes = SchoolClass.objects.filter(slug=class_slug)
    students = get_object_or_404(Student.objects.filter(slug=student_slug))
    if (students.present+students.cause+students.absent) > 0:
        total = round((students.present*100)/(students.present+students.cause+students.absent), 2)
    else:
        total = 0
    if request.user.is_superuser:
        if request.method == 'POST':
            if 'student_delete_btn' in request.POST:
                obj = students
                obj.delete()
                
            return  redirect('attendance:admin_class_detail',pk=schools.pk, slug=school_class.slug)
    context = {
        'schools':schools,
        'school_class':school_class,
        'classes':classes,
        'students': students,
        'total': total,
    }

    return render(request,'attendance/dashboard/admin_student_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def AdminUserDetailView(request, pk):
    teachers = get_object_or_404(Teacher.objects.all(), pk=pk)

    return render(request,'attendance/dashboard/user_detail.html', {'teachers':teachers})
   
@user_passes_test(lambda u: u.is_superuser)
def CreateUserView(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = TeacherForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password1 = user_form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            user = authenticate(username=username, password=password1)

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            School.objects.get_or_create(
                school_name = profile.work_place,
                principal = user,
            )

            registered = True

        
    else:
        user_form = UserForm()
        profile_form = TeacherForm()

    return render(request, 'attendance/dashboard/add_user.html', {
        'registered': registered,
        'user_form': user_form,
        'profile_form':profile_form
    })

class AdminAttendanceListView(LoginRequiredMixin, ListView):
    template_name = 'attendance/dashboard/admin_attendance_list.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(AdminAttendanceListView, self).get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['teachers'] = Teacher.objects.all()
        context['students'] = Student.objects.all()
        context['attendance'] = Attendance.objects.all()
        context['date'] = datetime.today().date()
        school_context = {}
        s_name = []
        s_a_student = []
        s_t_p = []
        s_t_c = []
        s_t_a = []
        s_t_pp = []
        s_t_cp = []
        s_t_ap = []
        s_a_s = []
        context['school_list'] = []
        for schoo in context['schools']:
            school = School.objects.filter(school_name=schoo)
            schools = get_object_or_404(School.objects.filter(school_name=schoo))
            school_attendance = Attendance.objects.filter(teacher__work_place=schoo, date=context["date"]).count()
            school_all_student = Student.objects.filter(student_school__in=school).count()
            s_name.append(schools)
            teacher = Teacher.objects.filter(work_place=schoo)
            if school_all_student >0:
                school_context['school_attendance_status'] = round((100 * school_attendance) / school_all_student, 2)
                s_a_s.append(school_context['school_attendance_status'])
                school_context['school_all_students'] = (Student.objects.filter(student_school__in=school).count())
                s_a_student.append(school_context['school_all_students'])
                school_all_students= (Student.objects.filter(student_school__in=school).count()) * (timezone.now().date().weekday() + 1)
                school_context['school_total_present'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance='Bor',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_p.append(school_context['school_total_present'])
                school_context['school_total_cause'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance='Sababli',teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_c.append(school_context['school_total_cause'])
                school_context['school_total_absent'] = Attendance.objects.filter(date__week=context['date'].isocalendar()[1], mark_attendance="Yo'q",teacher__in=teacher).exclude(date__week_day=1).count()
                s_t_a.append(school_context['school_total_absent'])
                school_context['school_total_ppercent'] = round(school_context['school_total_present'] * 100 / school_all_students, 2)
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = round(school_context['school_total_cause'] * 100 / school_all_students, 2)
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = round(school_context['school_total_absent'] * 100 / school_all_students, 2)
                s_t_ap.append(school_context['school_total_apercent'])

            else:
                school_context['school_all_students'] = "O'quvchi kiritilmagan"
                s_t_p.append(0)
                s_t_c.append(0)
                s_t_a.append(0)
                s_a_s.append(0)
                s_a_student.append(school_context['school_all_students'])
                school_context['school_total_ppercent'] = 0
                s_t_pp.append(school_context['school_total_ppercent'])
                school_context['school_total_cpercent'] = 0
                s_t_cp.append(school_context['school_total_cpercent'])
                school_context['school_total_apercent'] = 0
                s_t_ap.append(school_context['school_total_apercent'])
            
            context['school_list'] = zip(s_name, s_a_student, s_t_p, s_t_pp, s_a_s)
        
        return context

@user_passes_test(lambda u: u.is_superuser)
def AdminAttendanceReport(request, pk):
    schools = get_object_or_404(School.objects.all(), pk=pk)
    teacher = Teacher.objects.filter(work_place=schools)
    school_class = SchoolClass.objects.filter(class_school=schools)
    date = datetime.today().date()
    attendance = Attendance.objects.filter(date=datetime.today(),teacher__in=teacher)
    students=Student.objects.filter(student_teacher__in=teacher)

    studentMen = students.filter(student_gender='M')
    studentFemale = students.filter(student_gender='F')
    boys = attendance.filter(student__in=studentMen)
    girls = attendance.filter(student__in=studentFemale)
    p_boys = boys.filter(mark_attendance='Bor')
    p_girls = girls.filter(mark_attendance='Bor')
    c_boys = boys.filter(mark_attendance='Sababli')
    c_girls = girls.filter(mark_attendance='Sababli')
    a_boys = boys.filter(mark_attendance="Yo'q")
    a_girls = girls.filter(mark_attendance="Yo'q")

    boys_present = []
    girls_present = []
    boys_cause = []
    girls_cause = []
    boys_absent = []
    girls_absent = []
    total_present = []
    total_cause = []
    total_absent = []
    student_data = []
    for classes in school_class:
        st = students.filter(student_class=classes)
        student_data.append(st)
        stMen = st.filter(student_gender='M')
        stFemale = st.filter(student_gender='F')
        boy = attendance.filter(student__in=stMen)
        girl = attendance.filter(student__in=stFemale)
        boys_present.append(boy.filter(mark_attendance='Bor').count())
        girls_present.append(girl.filter(mark_attendance='Bor').count())
        boys_absent.append(boy.filter(mark_attendance="Yo'q").count())
        girls_absent.append(girl.filter(mark_attendance="Yo'q").count())
        boys_cause.append(boy.filter(mark_attendance='Sababli').count())
        girls_cause.append(girl.filter(mark_attendance='Sababli').count())
        total_present.append(boy.filter(mark_attendance='Bor').count() + girl.filter(mark_attendance='Bor').count())
        total_cause.append(boy.filter(mark_attendance='Sababli').count() + girl.filter(mark_attendance='Sababli').count())
        total_absent.append(boy.filter(mark_attendance="Yo'q").count() + girl.filter(mark_attendance="Yo'q").count())
        

    report_data = zip(school_class,boys_present, boys_absent,boys_cause,girls_present,girls_absent,girls_cause,total_present,total_absent,total_cause, student_data)
        
    context = {
            'date':date,
            'schools':schools,
            'school_class':school_class,
            'teacher':teacher,
            'attendance':attendance,          
            'p_boys':p_boys,
            'c_boys':c_boys,
            'a_boys':a_boys,
            'p_girls':p_girls,
            'c_girls':c_girls,
            'a_girls':a_girls,
            'report_data':report_data,
        }
    return render(request,'attendance/dashboard/admin_attendance_report.html',context)


@user_passes_test(lambda u: u.is_superuser)
def export_to_csv(request, pk):

    #Data For Report
    schools = get_object_or_404(School.objects.all(), pk=pk)
    teacher = Teacher.objects.filter(work_place=schools)
    school_class = SchoolClass.objects.filter(class_school=schools)
    attendance = Attendance.objects.filter(date=datetime.today(),teacher__in=teacher)
    students=Student.objects.filter(student_teacher__in=teacher)

    # CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}-report-{}.csv"'.format(schools.school_name, datetime.today().date())
    writer = csv.writer(response)
    writer.writerow(['Sinf', 'Yigitlar(Bor)', "Yigitlar(Yo'q)","Yigitlar(Sababli)", 'Qizlar(Bor)', "Qizlar(Yo'q)", "Qizlar(Sababli)",'Jami(Bor)', "Jami(Yo'q)","Jami(Sababli)" ])

    #Data Writing
    for classes in school_class:
        row = []
        st = students.filter(student_class=classes)
        stMen = st.filter(student_gender='M')
        stFemale = st.filter(student_gender='F')
        boy = attendance.filter(student__in=stMen)
        girl = attendance.filter(student__in=stFemale)
        row.append(classes.class_type)
        row.append(boy.filter(mark_attendance='Bor').count())
        row.append(boy.filter(mark_attendance="Yo'q").count())
        row.append(boy.filter(mark_attendance="Sababli").count())
        row.append(girl.filter(mark_attendance='Bor').count())
        row.append(girl.filter(mark_attendance="Yo'q").count())
        row.append(girl.filter(mark_attendance="Sababli").count())
        row.append(boy.filter(mark_attendance='Bor').count() + girl.filter(mark_attendance='Bor').count())
        row.append(boy.filter(mark_attendance="Yo'q").count() + girl.filter(mark_attendance="Yo'q").count())
        row.append(boy.filter(mark_attendance='Sababli').count() + girl.filter(mark_attendance='Sababli').count())
        writer.writerow(row)
    return response


# ##############################
#                              # 
#   Oddiy foydalanuvchi uchun  #
#                              # 
################################
class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'attendance/profile/index.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.filter(student_teacher=context['teacher'])
        context['classes'] = SchoolClass.objects.filter(class_teacher=context['teacher'])
        context['date'] = datetime.today().date()
        if context['students'].count() > 0:
            context['attendance_percent'] = round((100 * Attendance.objects.filter(teacher=context['teacher'], date=context['date'] ).count()/context['students'].count()),2)
        context["current_time"] = datetime.strftime(datetime.now(),"%H:%M:%S") 
        context["expired_time"] = "15:00:00"
        if context["current_time"] >= context["expired_time"]:
            context['is_expired'] = False
        elif context["current_time"] < context["expired_time"]:
            context['is_expired'] = True
        if Attendance.objects.filter(date=datetime.today().date(), teacher=context['teacher']).count() == 0 or timezone.now().date().weekday()==6:
            context['date'] = datetime.today().date() - timedelta(days=1)
        if context['students'].count() > 0:
            context['total_present'] = Attendance.objects.filter(date=context['date'], mark_attendance='Bor', teacher=context['teacher'] ).count()
            context['p_percent'] = round(((context['total_present'] * 100) / context['students'].count()), 2)
            context['total_cause'] = Attendance.objects.filter(date=context['date'], mark_attendance='Sababli', teacher=context['teacher'] ).count()
            context['c_percent'] = round(((context['total_cause'] * 100) / context['students'].count()), 2)
            context['total_absent'] = Attendance.objects.filter(date=context['date'], mark_attendance="Yo'q", teacher=context['teacher'] ).count()
            context['a_percent'] = round(((context['total_absent'] * 100) / context['students'].count()), 2)
            context['wp_label'], context['wa_label'], context['wc_label'], context['date_label'] = [], [], [], []
            context['mp_label'], context['ma_label'], context['mc_label'], context['monthly_date_label'] = [], [], [], []
            context['is_sunday'] = False
            for i in range(6,-1,-1):
                some_day_last_week = timezone.now().date() - timedelta(days=i)
                
                if some_day_last_week.weekday()!=6:
                    context['date_label'].append(datetime.strftime(datetime.now()- timedelta(i), '%d/%m/%y'))
                    present = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Bor', teacher=context['teacher'] ).count()
                    context['wp_label'].append(round(((present * 100) / context['students'].count()), 2))
                    cause = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Sababli', teacher=context['teacher'] ).count()
                    context['wc_label'].append(round(((cause * 100) / context['students'].count()), 2))
                    absent = Attendance.objects.filter(date=some_day_last_week, mark_attendance="Yo'q", teacher=context['teacher'] ).count()
                    context['wa_label'].append(round(((absent * 100) / context['students'].count()), 2))
                elif timezone.now().date().weekday() == 6:
                    context['is_sunday'] = True
                
            for i in range(31,-1,-1):
                some_day_last_week = timezone.now().date() - timedelta(days=i)
                if some_day_last_week.weekday()!=6:
                    context['monthly_date_label'].append(datetime.strftime(datetime.now()- timedelta(i), '%d/%m/%y'))
                    present = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Bor', teacher=context['teacher'] ).count()
                    context['mp_label'].append(round(((present * 100) / context['students'].count()), 2))
                    cause = Attendance.objects.filter(date=some_day_last_week, mark_attendance='Sababli', teacher=context['teacher'] ).count()
                    context['mc_label'].append(round(((cause * 100) / context['students'].count()), 2))
                    absent = Attendance.objects.filter(date=some_day_last_week, mark_attendance="Yo'q", teacher=context['teacher'] ).count()
                    context['ma_label'].append(round(((absent * 100) / context['students'].count()), 2))  
                elif timezone.now().date().weekday() == 6:
                    context['is_sunday'] = True
            context['wp_percent'] = round(sum(context['wp_label'])/len(context['wp_label']),2)
            context['mp_percent'] = round(sum(context['mp_label'])/len(context['mp_label']),2)
            context['wc_percent'] = round(sum(context['wc_label'])/len(context['wc_label']),2)
            context['mc_percent'] = round(sum(context['mc_label'])/len(context['mc_label']),2)
            context['wa_percent'] = round(sum(context['wa_label'])/len(context['wa_label']),2)
            context['ma_percent'] = round(sum(context['ma_label'])/len(context['ma_label']),2)

        return context

    def get_queryset(self):
        queryset = Teacher.objects.filter(user=self.request.user)
        test_queryset = School.objects.filter(principal=self.request.user)
        if queryset:
            return queryset
        elif test_queryset:
            queryset = Teacher.objects.filter(teacher_school=test_queryset)
            return queryset
        else:
            return queryset

@login_required
def TeacherClassListView(request, pk):
    teacher = get_object_or_404(Teacher.objects.filter(user=request.user))
    teachers = Teacher.objects.filter(pk=teacher.pk)
    students=Student.objects.filter(student_teacher__in=teachers)
    school_class = SchoolClass.objects.filter(class_teacher__in=teachers)
    class_percent_list = []
    class_list = []

    for classes in school_class:
        student_percent_list = []
        
        classe = get_object_or_404(SchoolClass.objects.filter(slug=classes.slug))
        student_classes = SchoolClass.objects.filter(slug=classes.slug)
        studenta = Student.objects.filter(student_class__in=student_classes)
        for student in studenta:
            studente = get_object_or_404(Student.objects.filter(pk=student.pk, student_class=classes))
            present = studente.present
            cause = studente.cause
            absent = studente.absent
            if (present + absent + cause) > 0:
                student_percent = round((100 * present) / (present + absent + cause),2)
            else:
                student_percent = 0 
            student_percent_list.append(student_percent)
        if len(student_percent_list) > 0:    
            class_percent_list.append(round((sum(student_percent_list)/len(student_percent_list)),2))
        else: 
            class_percent_list.append(0)
        class_list.append(classe)
    about_class = zip(class_list, class_percent_list)
    context = {
        'teacher':teacher, 
        'school_class':school_class,
        'students':students, 
        'about_class':about_class}
    return render(request,'attendance/profile/class_list.html', context)

@login_required
def TeacherAttendanceListView(request, pk):

    current_time = datetime.strftime(datetime.now(),"%H:%M:%S") 
    expired_time = "16:00:00"
    teacher = get_object_or_404(Teacher.objects.filter(user=request.user))
    teachers = Teacher.objects.filter(pk=teacher.pk)
    date = datetime.today().date()
    students=Student.objects.filter(student_teacher__in=teachers)
    school_class = SchoolClass.objects.filter(class_teacher__in=teachers)
    class_st_list, class_ty_list, is_done_list, class_pk, expire_list= [], [], [], [], []
    for classes in school_class:
        if current_time < expired_time:
            is_expired = False
        elif current_time >= expired_time:
            is_expired = True
        expire_list.append(is_expired)
        classss = SchoolClass.objects.filter(pk = classes.pk)
        class_pk.append(classes.slug)
        student_count = Student.objects.filter(student_class__in=classss).count()
        class_st_list.append(student_count)
        is_done = False
        class_ty_list.append(classes.class_type)
        class_student = [student.pk for student in Student.objects.filter(student_class__in=classss)]
        class_attendance = [attendance.student.pk for attendance in Attendance.objects.filter(date=date,teacher__teacher_class__in=classss)]
        if list(set(class_student) - set(class_attendance)) == []:
            is_done = True
        is_done_list.append(is_done)


    total_report = zip( class_ty_list, class_st_list, is_done_list, class_pk, expire_list)



    context={
        'teacher':teacher, 
        'school_class':school_class,
        'students':students, 
        'attendance_form':attendance_form, 
        'total_report':total_report,
        'expire_list':expire_list,
        'is_expired':is_expired,
        }
    return render(request,'attendance/profile/attendance_list.html', context)


@login_required
def TeacherStudentDetailView(request, pk, class_slug, student_slug):
    teacher = get_object_or_404(Teacher.objects.filter(pk=pk))
    teachers = Teacher.objects.filter(pk=pk)
    school_class = get_object_or_404(SchoolClass.objects.filter(slug=class_slug))
    classes = SchoolClass.objects.filter(slug=class_slug)
    students = get_object_or_404(Student.objects.filter(slug=student_slug))
    if (students.present+students.cause+students.absent) > 0:
        total = round((students.present*100)/(students.present+students.cause+students.absent), 2)
    else:
        total = 0
    if teacher.user == request.user:
        if request.method == 'POST':
            if 'student_delete_btn' in request.POST:
                obj = students
                obj.delete()
                    
            return  redirect('attendance:teacher_class_detail',pk=teacher.pk, slug=school_class.slug)
    context = {
        'teacher':teacher,
        'teachers':teachers,
        'school_class':school_class,
        'classes':classes,
        'students': students,
        'total': total,
    }

    return render(request,'attendance/profile/teacher_student_detail.html', context)


@login_required
def TeacherClassDetailView(request,pk, slug):
    teacher = get_object_or_404(Teacher.objects.filter(pk=pk))
    teachers = Teacher.objects.filter(pk=pk)
    class_school = get_object_or_404(SchoolClass.objects.filter(slug=slug, class_teacher=teacher))
    all_class = SchoolClass.objects.filter(class_teacher=teacher)
    
    students = Student.objects.filter(student_class=class_school)
    count = students.count()
    date = datetime.today().date().strftime('%d-%m-%Y')

    if slug==class_school.slug:
        student_percent_list = []
        student_list = []

        for student in students:
            studente = get_object_or_404(Student.objects.filter(slug=student.slug))
            present = studente.present
            cause = studente.cause
            absent = studente.absent
            if (present + absent + cause) > 0:
                student_percent = round((100 * present) / (present + absent + cause),2)
            else:
                student_percent = 0 
            student_percent_list.append(student_percent)
            student_list.append(studente)
        about_student = zip(student_list, student_percent_list)
    

        sc_form = StudentForm(request.POST or None)
        cc_form = ClassForm(request.POST or None)
        scf_form = CsvModelForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if 'student_create_btn' in request.POST:
                if sc_form.is_valid():
                    s_create = sc_form.save(commit=False)
                    s_create.student_class = class_school
                    s_create.student_teacher = teacher
                    s_create.student_school = class_school.class_school
                    s_create.save()


            elif 'clas_delete_btn' in request.POST:
                obj = class_school
                obj.delete()
                return  redirect('attendance:teacher_class_detail',pk=teacher.pk)

            return  redirect('attendance:teacher_class_detail',pk=teacher.pk, slug=class_school.slug)

        context = {
            'teachers':teachers,
            'teacher':teacher,
            'class_school':class_school,

            'students': students,
            'sc_form':sc_form,
            'scf_form':scf_form,
            'cc_form':cc_form,
            'about_student':about_student,
        }

        return render(request,'attendance/profile/teacher_class_detail.html', context)
    return render(request,'attendance/profile/teacher_class_detail.html', context)
    

class TeacherProfileView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'attendance/profile/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherProfileView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.filter(student_teacher=context['teacher'])
        # context['teacher'] = Student.objects.all()
        return context

    def get_queryset(self):
        queryset = Teacher.objects.filter(user=self.request.user)
        test_queryset = School.objects.filter(principal=self.request.user)
        if queryset:
            return queryset
        elif test_queryset:
            queryset = Teacher.objects.filter(teacher_school=test_queryset)
            return queryset
        else:
            return queryset

class TeacherProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'attendance/profile/user_profile_update.html'
    model = Teacher
    form_class = TeacherUpdateForm
    login_url = '/login/'

    def get_queryset(self):
        queryset = Teacher.objects.filter(user=self.request.user)
        return queryset


@login_required
def TeacherAttendanceReportView(request, pk):
  
    teacher = get_object_or_404(Teacher.objects.filter(user=request.user))
    teachers = Teacher.objects.filter(pk=teacher.pk)

    if teacher.user == request.user:
        school_class = SchoolClass.objects.filter(class_teacher__in=teachers)
        date = datetime.today().date()
        attendance = Attendance.objects.filter(date=datetime.today(),teacher__in=teachers)
        students=Student.objects.filter(student_teacher__in=teachers)

        studentMen = students.filter(student_gender='M')
        studentFemale = students.filter(student_gender='F')
        boys = attendance.filter(student__in=studentMen)
        girls = attendance.filter(student__in=studentFemale)
        p_boys = boys.filter(mark_attendance='Bor')
        p_girls = girls.filter(mark_attendance='Bor')

        a_boys = boys.filter(mark_attendance="Yo'q")
        a_girls = girls.filter(mark_attendance="Yo'q")
        c_boys = boys.filter(mark_attendance='Sababli')
        c_girls = girls.filter(mark_attendance='Sababli')

        #For detailed report
        boys_present = []
        girls_present = []
        boys_cause = []
        girls_cause = []
        boys_absent = []
        girls_absent = []
        total_present = []
        total_cause = []
        total_absent = []
        student_data = []

        for classes in school_class:
            st = students.filter(student_class=classes)
            student_data.append(st)
            stMen = st.filter(student_gender='M')
            stFemale = st.filter(student_gender='F')
            boy = attendance.filter(student__in=stMen)
            girl = attendance.filter(student__in=stFemale)
            boys_present.append(boy.filter(mark_attendance='Bor').count())
            girls_present.append(girl.filter(mark_attendance='Bor').count())

            boys_absent.append(boy.filter(mark_attendance="Yo'q").count())
            girls_absent.append(girl.filter(mark_attendance="Yo'q").count())
            boys_cause.append(boy.filter(mark_attendance='Sababli').count())
            girls_cause.append(girl.filter(mark_attendance='Sababli').count())
            total_present.append(boy.filter(mark_attendance='Bor').count() + girl.filter(mark_attendance='Bor').count())
            total_cause.append(boy.filter(mark_attendance='Sababli').count() + girl.filter(mark_attendance='Sababli').count())
            total_absent.append(boy.filter(mark_attendance="Yo'q").count() + girl.filter(mark_attendance="Yo'q").count())
        
        report_data = zip(school_class,boys_present, boys_absent,boys_cause,girls_present,girls_absent,girls_cause,total_present,total_absent,total_cause, student_data)
        
    context = {
            'date':date,
            'school_class':school_class,
            'teacher':teacher,
            'attendance':attendance,          
            'p_boys':p_boys,
            'a_boys':a_boys,
            'c_boys':c_boys,
            'p_girls':p_girls,
            'a_girls':a_girls,
            'c_girls':c_girls,
            'report_data':report_data,
        }
    return render(request,'attendance/profile/user_attendance_report.html',context)
        

@login_required
def attendance_form(request,pk, slug):
    teacher = get_object_or_404(Teacher.objects.filter(pk=pk))
    class_school = get_object_or_404(SchoolClass.objects.filter(slug=slug, class_teacher=teacher))
    
    students = Student.objects.filter(student_class=class_school)
    count = students.count()
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')

    if slug==class_school.slug:
        if request.method == 'POST':
            formset = attendance_formset(request.POST)
            list = zip(students,formset)

            if formset.is_valid():
                for form, student in zip(formset,students):
                    date = datetime.today()
                    mark = form.cleaned_data['mark_attendance']  
                    check_attendance = Attendance.objects.filter(teacher=teacher,date=date,student=student)

                    if check_attendance:
                        attendance = Attendance.objects.get(teacher=teacher,date=date,student=student)
                        if attendance.mark_attendance == "Yo'q":
                            student.absent = student.absent - 1
                        elif attendance.mark_attendance == 'Bor':
                            student.present = student.present - 1
                        elif attendance.mark_attendance == 'Sababli':
                            student.cause = student.cause - 1
                        attendance.mark_attendance = mark
                        attendance.save()

                    else: 
                        attendance = Attendance()
                        attendance.teacher = teacher
                        attendance.student = student
                        attendance.date = date
                        attendance.mark_attendance = mark
                        attendance.save()

                    if mark == "Yo'q":
                        student.absent = student.absent + 1
         
                    elif mark == 'Bor':
                        student.present = student.present + 1
             
                    elif mark == 'Sababli':
                        student.cause = student.cause + 1
                    student.save()


                context = {
                    'students': students,
                    'teacher': teacher,
                }
                # return render(request, 'attendance/profile.html', context)
                return redirect('attendance:attendance_list', pk=teacher.pk)
            else:
                error = "Something went wrong"
                context = {
                    'error': error,
                    'formset': formset,
                    'students': students,
                    'teacher': teacher,
                    'list': list,
                    'date':date,
                }
                return render(request, 'attendance/profile/attendance_form1.html', context)

        else:
            list = zip(students, attendance_formset())
            context = {
                'formset': attendance_formset(),
                'students': students,
                'teacher': teacher,
                'class_school': class_school,
                'list': list,
                'date':date,
            }

            return render(request, 'attendance/profile/attendance_form1.html', context)

    else:
        return HttpResponse(status=403)


class TeacherSchoolRankingView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'attendance/profile/teacher_attendance_ranking.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherSchoolRankingView, self).get_context_data(**kwargs)
        context['students'] = Student.objects.filter(student_teacher=context['teacher'])
        context['classes'] = SchoolClass.objects.filter(class_teacher=context['teacher'])
        context['date'] = datetime.today().date()
        class_list, student_list, day_list, week_list = [], [], [], []
        for classe in context['classes']:
            t_d_p = 0
            class_list.append(classe.class_type)
            class_student = Student.objects.filter(student_class=classe)
            student_list.append(class_student.count())
            today_attendance = Attendance.objects.filter(date=context['date'], teacher__teacher_class=classe)
            for i in today_attendance:
                
                if (classe.class_type) == i.student.student_class.class_type:
                    if i.mark_attendance == 'Bor':
                        t_d_p += 1
            if class_student.count() > 0 and t_d_p > 0:           
                d_c_a = round((100 * t_d_p)/class_student.count(),2)
            else:
                d_c_a = "Natija topilmadi"
            day_list.append(d_c_a)
        for classe in context['classes']:
            t_w_p = 0
            class_student = Student.objects.filter(student_class=classe)
            week_attendance = Attendance.objects.filter(date__week=context['date'].isocalendar()[1],teacher__teacher_class=classe).exclude(date__week_day=1)
            for i in week_attendance:
                if (classe.class_type) == i.student.student_class.class_type and i.mark_attendance == 'Bor':
                    t_w_p += 1            
            if class_student.count() > 0 and t_w_p > 0:
                if datetime.today().weekday()<6:
                    w_c_a = round((100 * t_w_p)/(class_student.count() * (datetime.today().weekday() + 1)), 2)
                elif datetime.today().weekday()==6:    
                    w_c_a = round((100 * t_w_p)/(class_student.count() * (datetime.today().weekday())), 2)

            else:
                w_c_a = 0
            week_list.append(w_c_a)

        context["ranking"] = zip(class_list, student_list, day_list, week_list  )
            
        return context





class AllSchoolsRankingView(LoginRequiredMixin, DetailView):
    template_name = 'attendance/profile/schools_ranking_list.html'
    model = Teacher
    def get_context_data(self, **kwargs):  
        context = super(AllSchoolsRankingView, self).get_context_data(**kwargs)
        context['all_schools'] = School.objects.all()
        context['date'] = datetime.today().date()
        class_list, student_list, day_list, week_list = [], [], [], []
        for classe in context['all_schools']:
            t_d_p = 0
            class_list.append(classe.school_name)
            class_student = Student.objects.filter(student_school=classe)
            student_list.append(class_student.count())
            today_attendance = Attendance.objects.filter(date=context['date'], student__student_school=classe)
            for i in today_attendance:
                
                if (classe.school_name) == i.student.student_school.school_name:
                    if i.mark_attendance == 'Bor':
                        t_d_p += 1
            if class_student.count() > 0 and t_d_p > 0:           
                d_c_a = round((100 * t_d_p)/class_student.count(),2)
            else:
                d_c_a = "Natija topilmadi"
            day_list.append(d_c_a)
        for classe in context['all_schools']:
            t_w_p = 0
            class_student = Student.objects.filter(student_school=classe)
            week_attendance = Attendance.objects.filter(date__week=context['date'].isocalendar()[1],student__student_school=classe).exclude(date__week_day=1)
            for i in week_attendance:
                if (classe.school_name) == i.student.student_school.school_name and i.mark_attendance == 'Bor':
                    t_w_p += 1            
            if class_student.count() > 0 and t_w_p > 0:
                if datetime.today().weekday()<6:
                    w_c_a = round((100 * t_w_p)/(class_student.count() * (datetime.today().weekday() + 1)), 2)
                elif datetime.today().weekday()==6:    
                    w_c_a = round((100 * t_w_p)/(class_student.count() * (datetime.today().weekday())), 2)

            else:
                w_c_a = 0
            week_list.append(w_c_a)

        context["ranking"] = zip(class_list, student_list, day_list, week_list  )
            
        return context















# ##############################
#                              # 
#   Umumiy                     #
#                              # 
################################
# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active and not user.is_superuser:
                login(request, user)
                teachers = get_object_or_404(Teacher, user=user)
                return redirect('attendance:profile', pk=teachers.pk)
            elif user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('attendance:dashboard'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")

        else:
            return render(request, 'attendance/index.html', {'error_message': 'Invalid login'})
    
    return render(request, 'attendance/index.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active and not user.is_superuser:
                login(request, user)
                teachers = get_object_or_404(Teacher, user=user)
                return redirect('attendance:profile', pk=teachers.pk)
            elif user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('attendance:dashboard'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")

        else:
            return render(request, 'attendance/index.html', {'error_message': 'Invalid login'})
    return render(request, 'attendance/index.html',{})

def logout_user(request):
    logout(request)
    return redirect('attendance:index')

def custom_page_not_found_view(request, exception):
    return render(request, "attendance/errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "attendance/errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "attendance/errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "attendance/errors/400.html", {})

