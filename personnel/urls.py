from django.urls import path
from personnel import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("login/", views.login,name='login'),
    path("postuler/", views.postuler,name='postuler'),
    path("logout/",views.custom_logout,name='logout'),
    path("register/", views.register,name='register'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
    path("candidature/<str:username>/", views.candidature,name='candidature'),
    path("modifier/<str:username>/", views.update, name='update'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

