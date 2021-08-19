from django.urls import path
from . import views

app_name = 'pfreers'

urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:PfreeEateries_id>/', views.detail),
    path('create/', views.PfreeEateries_create, name='PfreeEateries_create'),
    path('update/', views.PfreeEateries_update, name='PfreeEateries_update'),
]