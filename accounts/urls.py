from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import home, login

urlpatterns = [    
    path('', login.as_view() , name='login'),                          
    path('login/', login.as_view() , name='login'),
    path('home/', home.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'), 
]    


