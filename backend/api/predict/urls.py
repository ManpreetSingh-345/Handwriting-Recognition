from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.predictRoute, name="predict"),
    path("api/get-csrf/", views.get_csrf_token, name='get_csrf_token'),
]
