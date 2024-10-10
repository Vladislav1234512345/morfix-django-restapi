from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileUpdateView,
    ProfileRetrieveView,
    ProfileImageCreateView,
    ProfileImageDeleteView,
    ProfileImageRetrieveView,
    ProfileImageListView
)

from . import views

urlpatterns = [
    # Пути до изображений профилей
    path('images/<int:pk>/delete/', ProfileImageDeleteView.as_view(), name='image-delete'),
    path('images/<int:pk>/', ProfileImageRetrieveView.as_view(), name='image'),
    path('images/add/', ProfileImageCreateView.as_view(), name='image-add'),
    path('images/', ProfileImageListView.as_view(), name='images'),

    # Пути до профилей
    path('create/', ProfileCreateView.as_view() , name='create'),
    path('update/', ProfileUpdateView.as_view() , name='update'),
    path('get_profiles/', views.get_profiles, name='get_profiles'),
    path('', ProfileRetrieveView.as_view(), name='detail'),
]