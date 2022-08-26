from django import template


register = template.Library()


# Тэг, который берет текущие параметры запроса и по указанному аргументу производит
# замену, не очищая остальные параметры.
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
