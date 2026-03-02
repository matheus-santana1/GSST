from urllib.parse import urlencode

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import RedirectView

from GSST.views import (acessar_arquivo, arquivo_view, check_cpf,
                        exportar_pdf_logs, login_cpf_view, logout)


class PasswordChangeViewCustom(auth_views.PasswordChangeView):
    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={self.request.get_host()},
        ):
            url = reverse("password_change_done")
            params = urlencode({"next": next_url})
            return f"{url}?{params}"
        return reverse("admin:index")
urlpatterns = [
    path("admin/logout/", logout, name="admin_logout"),
    path("admin/password_change/", PasswordChangeViewCustom.as_view(), name="admin_password_change", ),
    path('admin/', admin.site.urls),
    path('arquivo/<uuid:arquivo_id>/', acessar_arquivo, name='acessar_arquivo'),
    path('arquivo/view/<uuid:arquivo_id>/', arquivo_view, name='arquivo_view'),
    path('arquivo/<uuid:arquivo_id>/pdf/', exportar_pdf_logs, name='exportar_pdf_logs'),
    path('login/', login_cpf_view, name='login_cpf_view'),
    path("", RedirectView.as_view(url="/admin/", permanent=True)),
    path("password-change/", PasswordChangeViewCustom.as_view(), name="password_change", ),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done", ),
    path('api/check-cpf/', check_cpf, name='check_cpf'),
]
