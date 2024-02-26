from django.urls import path
from myapp import views

urlpatterns = [
  path("submit_data/", views.submit_data, name="submit_data"),
  # path("get_ntn/", views.get_ntn, name="get_ntn"),
  # path("get_ntn/<int:pk>", views.get_ntn, name="get_ntn"),
  path('filter/', views.FilterView.as_view(), name='filter-view'),
  path("missing_invoices/", views.missing_invoices, name="missing_invoices"),
]