from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('errors/', views.errors_index, name='index'),
  path('errors/<int:error_id>/', views.errors_detail, name='error_detail'),
  path('errors/create/', views.ErrorCreate.as_view(), name='error_create'),
  path('errors/<int:pk>/update/', views.ErrorUpdate.as_view(), name='error_update'),
  path('errors/<int:pk>/delete/', views.ErrorDelete.as_view(), name='error_delete'),
  path('errors/<int:error_id>/add_comment/', views.add_comment, name='add_comment'),
  path('errors/<int:error_id>/add_screenshot/', views.add_screenshot, name='add_screenshot'),
  path('errors/profile/', views.user_profile, name='user_profile'),
  path('errors/search', views.search, name='search'),
  path('accounts/signup/', views.signup, name='signup'),
  path('challenges/', views.challenges_index, name='challenge_index'),
  path('challenges/<int:challenge_id>', views.challenge_detail, name='challenge_detail'),
  path('scrape/', views.scrape, name='scrape'),
]