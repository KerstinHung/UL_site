from django import template

register = template.Library()

@register.filter(name="yesno_o")
def yesno_o(value):
    """
    If value is True -> Return 'Ｏ'
    Else -> Return blank (Use &nbsp; to stuff grid)
    """
    return "Ｏ" if value else "\u00A0"  # \u00A0 = blank w/o \rn (&nbsp;)
