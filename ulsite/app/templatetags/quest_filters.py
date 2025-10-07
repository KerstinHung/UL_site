from django import template

register = template.Library()

@register.filter(name="yesno_o")
def yesno_o(value):
    """
    如果 value 為 True -> 回傳 'Ｏ'
    否則 -> 回傳空白 (用 &nbsp; 讓表格格子不會塌縮)
    """
    return "Ｏ" if value else "\u00A0"  # \u00A0 = 不斷行空白 (&nbsp;)
