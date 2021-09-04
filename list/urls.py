from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addtolist", views.list_new, name="new_listing"),
    path("modifylist/<str:id>",views.modify_list, name = "modify_list"),

]
