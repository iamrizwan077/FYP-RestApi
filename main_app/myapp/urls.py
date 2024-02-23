from django.urls import path
from myapp import views

urlpatterns = [
  path("submit_data/", views.submit_data, name="submit_data"),
  path('filter/', views.FilterView.as_view(), name='filter-view'),
]