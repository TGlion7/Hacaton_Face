from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PostViewSet
from .views import admin_required, UserListView

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('check-face/', admin_required(views.check_face), name='check_face'),
    path('logout/', views.logout_view, name='logout'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('visit-log/', views.visit_log, name='visit_log'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)