from django.urls import path
from auth_user import views

urlpatterns = [
    path('login',views.LoginUser.as_view()),
]