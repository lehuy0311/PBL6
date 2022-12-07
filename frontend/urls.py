from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('blog/<int:pk>', PostDetailView.as_view(), name='post'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('blog/<int:pk>/edit', UpdatePostView.as_view(), name='update_post'),
    path('blog/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>', CategoryView, name='category'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password_success', password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page')
]
