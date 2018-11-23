from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaTesourosView.as_view(), name='list'),
    path('new', views.SalvarTesouroView.as_view(), name='new'),
    path('delete/<int:pk>', views.DeletarTesouroView.as_view(), name='delete'),
    path('edit/<int:pk>', views.SalvarTesouroView.as_view(), name='edit'),
]
