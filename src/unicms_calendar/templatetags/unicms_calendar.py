from django import template

register = template.Library()


@register.filter
def modulus(num, val):
    print("aaaaaaaaaaaa", num % val)
    return num % val
