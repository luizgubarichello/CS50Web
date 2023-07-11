from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF


def validate_cpf(value):

    # Check if it has 11 digits
    cpf = str(value)
    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter 11 digitos.')
    
    # Check if the CPF sequence is valid
    fatia_um = cpf[:3]
    fatia_dois = cpf[3:6]
    fatia_tres = cpf[6:9]
    fatia_quatro = cpf[9:]

    cpf_formatado = "{}.{}.{}-{}".format(
        fatia_um,
        fatia_dois,
        fatia_tres,
        fatia_quatro
    )

    cpfv = CPF()
    if not cpfv.validate(cpf_formatado):
        raise ValidationError(
            _('%(value)s nao e valido.'),
            params={'value': cpf_formatado},
        )

