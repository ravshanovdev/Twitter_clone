from django.urls import path
from .views import homepage, profile_list, profile, login_user, logout_user, \
                   register_user, update_user, meep_like, meep_show, unfollow,\
                   follow, followers, follows, delete_meep, update_meep, search,\
                   search_user


urlpatterns = [
    path('', homepage, name='home'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/followers/<int:pk>', followers, name='followers'),
    path('profile/follows/<int:pk>', follows, name='follows'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('update_user/', update_user, name='update_user'),
    path('meep_like/<int:pk>/', meep_like, name='meep_like'),
    path('meep_show/<int:pk>/', meep_show, name='show_meep'),
    path('unfollow/<int:pk>/', unfollow, name='unfollow'),
    path('follow/<int:pk>/', follow, name='follow'),
    path('delete_meep/<int:pk>/', delete_meep, name='delete_meep'),
    path('update_meep/<int:pk>/', update_meep, name='update_meep'),
    path('search/', search, name='search'),
    path('search_user/', search_user, name='search_user'),

]
