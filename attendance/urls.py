from django.urls import path
from . import views


app_name = 'attendance'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'login/', views.login_user, name='login_user'),
    path(r'logout/', views.logout_user, name='logout_user'),

    # ##############################
    #                              # 
    #     Administrator uchun      #
    #                              # 
    ################################
    path(r'dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
    path(r'dashboard/school_list/', views.AdminSchoolListView.as_view(), name='admin_school_list'),
    path(r'dashboard/admin_attendance_list/', views.AdminAttendanceListView.as_view(), name='admin_attendance_list'),
    path(r'dashboard/admin_attendance_list/(?P<pk>[0-9]+)/admin_attendance_report/', views.AdminAttendanceReport, name='admin_attendance_report'),
    path(r'dashboard/admin_attendance_list/(?P<pk>[0-9]+)/admin_attendance_report/download/', views.export_to_csv, name='export_to_csv'),
    path(r'dashboard/add_user/', views.CreateUserView, name='admin_add_user'),
    path(r'dashboard/user_detail/(?P<pk>[0-9]+)/', views.AdminUserDetailView, name='admin_user_detail'),
    path(r'dashboard/school_detail/(?P<pk>[0-9]+)/', views.AdminSchoolDetailView, name='admin_school_detail'),
    path(r'dashboard/school_detail/(?P<pk>[0-9]+)/admin_class_detail/(?P<slug>[0-9]+)/', views.ClassDetailView, name='admin_class_detail'),
    path(r'dashboard/school_detail/(?P<pk>[0-9]+)/admin_class_detail/(?P<str:class_slug>[0-9]+)/admin_student_detail/(?P<slug:student_slug>(0-9)+)/', views.AdminStudentDetailView, name='admin_student_detail'),
    
    # ##############################
    #                              # 
    #   Oddiy foydalanuvchi uchun  #
    #                              # 
    ################################
    path(r'profile/(?P<pk>[0-9]+)/', views.TeacherDetailView.as_view(), name='profile'),
    path(r'profile/(?P<pk>[0-9]+)/teacher_class_list/', views.TeacherClassListView, name='teacher_class_list'),
    path(r'profile/(?P<pk>[0-9]+)/attendance_form1/(?P<slug>[0-9]+)/', views.attendance_form, name='attendance_form1'),
    path(r'profile/(?P<pk>[0-9]+)/user_attendance_report/', views.TeacherAttendanceReportView, name='user_attendance_report'),
    path(r'profile/profile_detail/(?P<pk>[0-9]+)/', views.TeacherProfileView.as_view(), name='profile_detail'),
    path(r'profile/profile_detail/(?P<pk>[0-9]+)/user_profile_update/', views.TeacherProfileUpdateView.as_view(), name='user_profile_update'),
    
]