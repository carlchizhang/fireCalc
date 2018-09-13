from django.urls import path
from . import views

app_name = 'calc'
urlpatterns = [
    path('', views.calc, name='calc'),
    path('about/', views.about, name='about'),
    path('calc-pre/', views.calc_pre, name='calc-pre'),
    path('calc-post/', views.calc_post, name='calc-post'),
]
