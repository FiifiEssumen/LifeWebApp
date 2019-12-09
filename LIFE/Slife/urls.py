from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.urls import reverse

from Slife import views


app_name = 'Slife'
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    #path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login/',views.my_login,name='login'),
    path('logout/',views.my_logout,name='logout'),
    path('about/',views.about,name='about'),


    #password reset urls
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='Slife/password_reset_done.html',
    email_template_name='password_reset_email.html ',
    success_url=reverse_lazy('Slife:password_reset_done')),

    name='password_reset'),

   path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Slife/password_reset_done.html'),
    name='password_reset_done' ),
   path('password-reset-confirm/<uidb64>/<token>/',
   auth_views.PasswordResetConfirmView.as_view(template_name='Slife/password_reset_confirm.html',
                                                             success_url = reverse_lazy('Slife:password_reset_complete')
   ),name='password_reset_complete'), 


    path('categories/all/', views.all_categories,name='categories'),
    path('search/', views.search,name='search'),
    path('contact/', views.contact,name='contact'),
    path('<slug>/', views.options, name='options'),
    path('<slug>/comment/', views.comment, name='comment'),
    path('<slug>/vote/', views.vote, name='vote'),
    path('api/categories', views.api_categories,name='api_categories'),
    path('api/options/', views.api_options,name='api_options'),




]