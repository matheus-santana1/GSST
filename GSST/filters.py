import django_filters

from .models import LogAcesso, Usuario


class LogFilter(django_filters.FilterSet):
    cr = django_filters.ChoiceFilter(field_name='usuario__cr', label='CR', empty_label="Todos os CRs",
                                     choices=Usuario.CR_CHOICES)

    class Meta:
        model = LogAcesso
        fields = ['cr']
