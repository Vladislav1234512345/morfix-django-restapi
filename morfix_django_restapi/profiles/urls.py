from django.urls import path

from . import views

urlpatterns = [
    # Пути до хобби профилей
    path('hobbies/list/', views.get_hobbies_list, name='hobbies-list'),
    path('hobbies/add/', views.ProfileHobbyCreateView.as_view(), name='hobbie-add'),
    path('hobbies/<int:pk>/delete/', views.ProfileHobbyDeleteView.as_view(), name='hobbie-delete'),
    path('hobbies/', views.ProfileHobbyListView.as_view(), name='hobbies'),

    # Пути до изображений профилей
    path('images/<int:pk>/delete/', views.ProfileImageDeleteView.as_view(), name='image-delete'),
    path('images/<int:pk>/', views.ProfileImageRetrieveView.as_view(), name='image'),
    path('images/add/', views.ProfileImageCreateView.as_view(), name='image-add'),
    path('images/', views.ProfileImageListView.as_view(), name='images'),

    # Пути до профилей
    path('create/', views.ProfileCreateView.as_view() , name='create'),
    path('update/', views.ProfileUpdateView.as_view() , name='update'),
    path('get_profiles/', views.get_profiles, name='get_profiles'),
    path('', views.ProfileRetrieveView.as_view(), name='detail'),
]