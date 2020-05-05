from django.urls import path
from v1.userapp.views.role import RoleList

urlpatterns = [
    path('', RoleList.as_view()),
    path('list/', RoleList.as_view())
]