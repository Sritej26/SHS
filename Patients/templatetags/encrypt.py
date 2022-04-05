from django import template
from django.core import signing

register=template.Library()

@register.filter
def patient_id_encrypt_tag(k,a):
    try:
        return signing.dumps(a)
    except:
        return ''