from django.urls import  path
from . import views
from .views import *
app_name = 'blog_app'


urlpatterns = [

    path('', views.index),
    path('create_user/', views.create_user, name='create_user'),
    path('user_logins/' , views.user_logins, name='user_logins'),
    path('logout/', views.user_logout, name='user_logout'),

    path('post_create/<int:id>', views.post_create, name="post_create"),
    path('post_fetch/<int:id>', views.post_fetch, name="post_fetch"),
    path('dashboard/<int:id>/', views.dashboard, name="dashboard"),
    path('update_post/<int:id>/<int:user_id>/', views.update_post, name="update_post"),
    path('delete_post/<int:post_id>/', views.delete_post, name="delete_post"),
    path('comment_create/',views.comment_create, name='comment_create'),

]