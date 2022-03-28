from django.urls import path
from rango import views


app_name = 'rango'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),

    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('collection/<username>/', views.MyCollectionView.as_view(), name='my_collection'),
    path('new_post/<username>/', views.MediumView.as_view(), name='new_post'),

    path('add_category/<username>/', views.AddCategoryRequestView.as_view(), name='add_category'),
    path('view_category_requests/<username>/', views.ShowCategoryRequestsView.as_view(), name='view_category_requests'),

    path('search/', views.search, name='search'),
    path('goto/', views.GotoView.as_view(), name='goto'),
    path('category/<category>/', views.MediaCategoryView.as_view(), name='category'),
    path('like_media/', views.LikeMediaView.as_view(), name='like_media'),
]
