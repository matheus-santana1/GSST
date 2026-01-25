import re

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as logout_func
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from weasyprint import HTML

from .filters import LogFilter
from .models import Arquivo, LogAcesso, Usuario


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
    logs = documento.logacesso_set.all().order_by('-data_acesso')
    filtro = LogFilter(request.GET, queryset=logs)
    context.update({
        'documento': documento,
        'title': f'Detalhes: {documento.titulo}',
        'logs': filtro.qs,
        'filter': filtro,
    })
    return render(request, 'arquivo_view.html', context)


@login_required
@staff_member_required
def exportar_pdf_logs(request, arquivo_id):
    documento = get_object_or_404(Arquivo, pk=arquivo_id)
    logs = documento.logacesso_set.all().order_by('-data_acesso')
    filtro = LogFilter(request.GET, queryset=logs)
    html_string = render_to_string('relatorios/logs_pdf.html', {
        'documento': documento,
        'logs': filtro.qs,
        'user': request.user
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="logs_{documento.id}.pdf"'
    HTML(string=html_string).write_pdf(response)
    return response


@require_POST
def logout(request):
    logout_func(request)
    return redirect('/login/')


@require_GET
def check_cpf(request):
    cpf_raw = request.GET.get('cpf', '')
    cpf_limpo = re.sub(r'[^0-9]', '', cpf_raw)
    data = {'exists': False, 'nome': ''}
    if len(cpf_limpo) == 11:
        try:
            user = Usuario.objects.get(cpf=cpf_limpo)
            if not user.has_usable_password():
                data['exists'] = True
                data['nome'] = user.nome_completo
                data['funcao'] = user.funcao
        except Usuario.DoesNotExist:
            pass
    return JsonResponse(data)
