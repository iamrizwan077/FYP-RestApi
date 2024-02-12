from django.urls import path
from myapp import views

urlpatterns = [
  path("anomaly", views.anomaly, name="anomaly"),
]