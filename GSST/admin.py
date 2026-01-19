
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .forms import CustomImportForm, UsuarioCreationForm
from .models import Arquivo, Usuario

admin.site.unregister(Group)


# noinspection PyUnresolvedReferences
class UsuarioResource(resources.ModelResource):
    hash_senha_padrao = None
    class Meta:
        model = Usuario
        import_id_fields = ('cpf',)
        fields = ('cpf', 'nome_completo', 'cr', 'funcao', 'categoria', 'pcd', 'aprendiz', 'data_de_admissao',
                  'data_de_demissao', 'situacao')
        use_bulk = True
        batch_size = 1000
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if 'cpf' in row:
            cpf_limpo = str(row['cpf']).replace('.', '').replace('-', '').strip()
            row['cpf'] = cpf_limpo

        if row.get('situacao') == 'ATIVO':
            row['is_active'] = True

    def before_import(self, dataset, **kwargs):
        senha_texto = getattr(settings, 'DEFAULT_IMPORT_PASSWORD')
        self.hash_senha_padrao = make_password(senha_texto)

    def before_save_instance(self, instance, row, **kwargs):
        if not instance.username:
            instance.username = instance.cpf
        if not instance.pk or not instance.password:
            instance.password = self.hash_senha_padrao

# noinspection PyDeprecation,PyAttributeOutsideInit
@admin.register(Usuario)
class CustomUserAdmin(ImportExportModelAdmin):
    formats = [base_formats.CSV]
    import_form_class = CustomImportForm
    add_form = UsuarioCreationForm
    resource_class = UsuarioResource

    list_display = ('cpf', 'nome_completo', 'cr', 'funcao', 'categoria', 'pcd', 'aprendiz',
                    'data_de_admissao', 'data_de_demissao', 'tempo_de_casa_visual', 'situacao', 'status_admin',
                    'botao_excluir',)
    list_filter = ()
    search_fields = ('cpf', 'first_name')
    ordering = ('first_name',)

    fieldsets = (
        ('Identificação', {'fields': ('cpf', 'nome_completo', 'email')}),
        ('Detalhes', {'fields': ('funcao', 'cr', 'categoria', 'situacao', 'pcd', 'aprendiz', 'data_de_admissao',
                                 'data_de_demissao')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    readonly_fields = ('tempo_de_casa_visual',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'nome_completo', 'cr', 'funcao', 'categoria', 'pcd', 'aprendiz', 'data_de_admissao',
                       'situacao', 'is_superuser', 'password1', 'password2'),
        }),
    )

    list_per_page = 50

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    @admin.display(description='Ações', ordering="nome_completo")
    def botao_excluir(self, obj):
        if obj == self.request.user:
            return ""
        opts = obj._meta
        url_name = f'admin:{opts.app_label}_{opts.model_name}_delete'
        url = reverse(url_name, args=[obj.pk])
        return format_html(
            '<a href="{}" class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></a>',
            url
        )

    @admin.display(description='Tempo de Casa', ordering='data_de_admissao')
    def tempo_de_casa_visual(self, obj):
        return obj.tempo_de_casa

    @admin.display(description='Admin', boolean=True, ordering='is_superuser')
    def status_admin(self, obj):
        return obj.is_superuser

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (
                self.secure_delete_selected,
                'delete_selected',
                "Deletar usuários selecionados"
            )
        return actions

    def secure_delete_selected(self, request, queryset, *args):
        if args:
            request = queryset
            queryset = args[0]
        if request.user in queryset:
            queryset = queryset.exclude(pk=request.user.pk)
            self.message_user(request, "Seu usuário foi removido da seleção para evitar auto-exclusão.",
                              level=messages.WARNING)
        if not queryset.exists():
            self.message_user(request, "Nenhum usuário válido para deletar.", level=messages.WARNING)
            return None
        return delete_selected(self, request, queryset)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request)
        if obj == request.user:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Arquivo)
class ArquivoSeguroAdmin(admin.ModelAdmin):
    list_display = ('visualizar', 'titulo', 'criado_em', 'link')

    @admin.display(description='#', ordering='titulo')
    def visualizar(self, obj):
        url = reverse('arquivo_view', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-outline-info btn-sm btn-" title="Visualizar Detalhes"><i class="fas fa-search"></i></a>',
            url)

    @admin.display(description='Link', ordering='titulo')
    def link(self, obj):
        url = reverse('acessar_arquivo', args=[obj.id])
        return format_html(
            '<a href="{}" target="_blank" class="btn btn-success btn-sm">Abrir Arquivo</a>',
            url
        )
