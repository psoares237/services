from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

# Importe as classes de views do seu services/views.py
from accounts.views import register_view, login_view, logout_view
from services.views import (
    ServiceListView,
    NewServiceCreateView,
    ServiceDetailView,
    ServiceUpdateView,
    ServiceDeleteView,
    # Se você tiver uma view 'blog_view' em outro lugar,
    # você precisará importá-la de lá ou defini-la.
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"), 
    path('logout/', logout_view, name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('services/', ServiceListView.as_view(), name='services'),
    path('services/new/', NewServiceCreateView.as_view(), name='new_service'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    # path('blog/', blog_view.as_view(), name='blog'), # Exemplo se blog_view também for uma classe
    # path('blog/', blog_view, name='blog'), # Exemplo se blog_view for uma função
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


