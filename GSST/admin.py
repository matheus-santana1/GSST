from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .forms import CustomImportForm, UsuarioCreationForm
from .models import Usuario

admin.site.unregister(Group)


# noinspection PyUnresolvedReferences
class UsuarioResource(resources.ModelResource):
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

    def before_save_instance(self, instance, row, **kwargs):
        if not instance.username:
            instance.username = instance.cpf
        if not instance.password:
            instance.set_unusable_password()

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

    @admin.display(description='Ações')
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

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request)
        if obj == request.user:
            return False
        return super().has_delete_permission(request, obj)
