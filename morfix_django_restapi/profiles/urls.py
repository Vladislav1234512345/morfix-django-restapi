from django.urls import path
from .views import ProfileCreateView, ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path('create/', ProfileCreateView.as_view() , name='create'),
    path('update/', ProfileUpdateView.as_view() , name='update'),
    path('', ProfileDetailView.as_view() , name='detail'),
]