from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from GSST.views import acessar_arquivo, arquivo_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('arquivo/<uuid:arquivo_id>/', acessar_arquivo, name='acessar_arquivo'),
    path('arquivo/view/<uuid:arquivo_id>/', arquivo_view, name='arquivo_view'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("", RedirectView.as_view(url="/admin/", permanent=True)),
    path("password-change/", auth_views.PasswordChangeView.as_view(), name="password_change", ),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done", ),
]
