from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from localflavor.br.models import BRCPFField


class Usuario(AbstractUser):
    CR_CHOICES = (
        ('71498 - MG - LPG - SRE - VALE CORR SUL LP ITABIRI - (GRSA)',
         '71498 - MG - LPG - SRE - VALE CORR SUL LP ITABIRI - (GRSA)'),
        ('74130 - MG - LPG - SRE - VALE CORR SUL LP NOV LIM - (GRSA)',
         '74130 - MG - LPG - SRE - VALE CORR SUL LP NOV LIM - (GRSA)'),
        ('71497 - MG - LPG - SRE - VALE CORRE SUL LP BRUMAD - (GRSA)',
         '71497 - MG - LPG - SRE - VALE CORRE SUL LP BRUMAD - (GRSA)'),
        ('71496 - MG - LPG - SRE - VALE CORREDOR SUL CONG - (GRSA)',
         '71496 - MG - LPG - SRE - VALE CORREDOR SUL CONG - (GRSA)'),
        ('79078 - MG - LPG - SRE - VALE CORR SUL LP NOV LIM - (GRSA)',
         '79078 - MG - LPG - SRE - VALE CORR SUL LP NOV LIM - (GRSA)'),
        ('71502 - MG - LPG - SRE - VALE CORR SUL LP OUR PRE - (GRSA)',
         '71502 - MG - LPG - SRE - VALE CORR SUL LP OUR PRE - (GRSA)'),
        ('71503 - MG - CAT - SRE - VALE CORR SUL LP NOV LIM - (GRSA)',
         '71503 - MG - CAT - SRE - VALE CORR SUL LP NOV LIM - (GRSA)'),
    )
    FUNCAO_CHOICES = (
        ('11033 - AJUDANTE DE SERVICOS GERAIS', '11033 - AJUDANTE DE SERVICOS GERAIS'),
        ('11365 - ENCARREGADO OPERACIONAL', '11365 - ENCARREGADO OPERACIONAL'),
        ('11626 - SUPERVISOR DE SERVICOS', '11626 - SUPERVISOR DE SERVICOS'),
        ('11089 - ASSISTENTE ADMINISTRATIVO I', '11089 - ASSISTENTE ADMINISTRATIVO I'),
        ('11486 - MEDICO DO TRABALHO', '11486 - MEDICO DO TRABALHO'),
        ('11168 - AUXILIAR DE SERVICOS GERAIS', '11168 - AUXILIAR DE SERVICOS GERAIS'),
        ('22531 - COORDENADOR OPERACIONAL', '22531 - COORDENADOR OPERACIONAL'),
        ('11377 - ENGENHEIRO DE SEGURANCA DO TRABALHO', '11377 - ENGENHEIRO DE SEGURANCA DO TRABALHO'),
        ('11668 - TECNICO DE SEGURANCA DO TRABALHO', '11668 - TECNICO DE SEGURANCA DO TRABALHO'),
        ('11088 - ASSISTENTE ADMINISTRATIVO', '11088 - ASSISTENTE ADMINISTRATIVO'),
        ('22189 - TECNICO DE SEGURANCA DO TRABALHO PL', '22189 - TECNICO DE SEGURANCA DO TRABALHO PL'),
    )
    CATEGORIA_CHOICES = (
        ('MENSALISTA', 'MENSALISTA'),
    )
    SITUACAO_CHOICES = (
        ('ADMISSAO FUTURA', 'ADMISSAO FUTURA'),
        ('ATIVO', 'ATIVO'),
        ('FERIAS', 'FERIAS'),
        ('TRANSFERIDO', 'TRANSFERIDO')
    )

    cpf = BRCPFField('CPF', unique=True)
    nome_completo = models.CharField('Nome Completo', max_length=255)
    cr = models.CharField('CR', choices=CR_CHOICES, blank=True, null=True, max_length=255)
    funcao = models.CharField('Função', choices=FUNCAO_CHOICES, blank=True, null=True, max_length=255)
    categoria = models.CharField('Categoria', choices=CATEGORIA_CHOICES, blank=True, null=True, max_length=255)
    pcd = models.BooleanField('PCD', default=False)
    aprendiz = models.BooleanField('Aprendiz', default=False)
    data_de_admissao = models.DateField('Data de Admissão', blank=True, null=True)
    data_de_demissao = models.DateField('Data de Demissão', blank=True, null=True)
    situacao = models.CharField('Situação', choices=SITUACAO_CHOICES, default='ATIVO', max_length=255)
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'nome_completo']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.nome_completo or self.first_name or self.cpf

    @property
    def tempo_de_casa(self):
        if not self.data_de_admissao:
            return "N/A"
        data_final = self.data_de_demissao if self.data_de_demissao else date.today()
        diferenca = data_final - self.data_de_admissao
        anos = diferenca.days // 365
        meses = (diferenca.days % 365) // 30
        if anos > 0:
            return f"{anos} anos e {meses} meses"
        elif meses > 0:
            return f"{meses} meses"
        else:
            return f"{diferenca.days} dias"

    def save(self, *args, **kwargs):
        self.username = self.cpf
        super().save(*args, **kwargs)
