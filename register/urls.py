from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("register/", views.register, name="register"),
#     path("login/", views.login, name="login")
# ]

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('delete/', views.delete),
    path('login/', views.login),
    path('users/', views.userList),
    path('users/update/', views.updateUser),
    path('logout/', views.logout),
    url(r'^my/datatable/data/$', views.OrderListJson.as_view(), name='order_list_json'),
    # path('authlogin/', views.auth_login),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)