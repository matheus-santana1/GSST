from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render

from .models import Arquivo, LogAcesso


@login_required
def acessar_arquivo(request, arquivo_id):
    usuario = request.user
    documento = get_object_or_404(Arquivo, pk=arquivo_id)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if usuario.is_authenticated and not (usuario.is_staff or usuario.is_superuser):
        LogAcesso.objects.get_or_create(
            usuario=usuario,
            arquivo=documento,
            defaults={"ip_usuario": ip}
        )
    return FileResponse(documento.arquivo, as_attachment=False)


@login_required
@staff_member_required
def arquivo_view(request, arquivo_id):
    documento = get_object_or_404(Arquivo, pk=arquivo_id)
    context = admin.site.each_context(request)
    fields = Arquivo._meta.fields
    logs = documento.logacesso_set.all().order_by('-data_acesso')
    context.update({
        'documento': documento,
        'title': f'Detalhes: {documento.titulo}',
        'fields': fields,
        'logs': logs
    })
    return render(request, 'arquivo_view.html', context)
