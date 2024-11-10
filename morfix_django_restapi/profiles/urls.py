from django.urls import path

from . import views

urlpatterns = [
    # Пути до хобби профилей
    path('hobbies-list/', views.get_hobbies_list, name='hobbies-list'),
    path('hobbies/add/', views.ProfileHobbyListCreateView.as_view(), name='profile-hobbies-add'),
    path('hobby/add/', views.ProfileHobbyCreateView.as_view(), name='hobby-add'),
    path('hobby/<int:pk>/delete/', views.ProfileHobbyDeleteView.as_view(), name='hobby-delete'),
    path('hobbies/', views.ProfileHobbyListView.as_view(), name='hobbies'),

    # Пути до изображений профилей
    path('image/<int:pk>/delete/', views.ProfileImageDeleteView.as_view(), name='image-delete'),
    path('image/<int:pk>/update/', views.ProfileImageUpdateView.as_view(), name='image-update'),
    path('image/<int:pk>/', views.ProfileImageRetrieveView.as_view(), name='image'),
    path('images/add/', views.profile_images_create, name='images-add'),
    path('images/', views.ProfileImageListView.as_view(), name='images'),

    # Пути до профилей
    path('create/', views.ProfileCreateView.as_view() , name='create'),
    path('update/', views.ProfileUpdateView.as_view() , name='update'),
    path('search-profiles/', views.search_profiles, name='search-profiles'),
    path('full-info/me/', views.my_profile_full_info, name='my-full-info'),
    path('full-info/<int:profile_id>/', views.profile_full_info, name='full-info'),
    path('', views.ProfileRetrieveView.as_view(), name='info'),

    # Пути для лайков
    path('likes/', views.received_likes_profiles, name='likes'), # Список лайков, которые были получены текущем профилем
    path('like/<int:pk>/delete/', views.delete_received_like, name='like-delete'), # Удаление лайка
    path('like/create/', views.create_like, name='like-create'), # Создание лайка
]

