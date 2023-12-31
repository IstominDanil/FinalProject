from django import template

register = template.Library()


# Тег, который позволяет не терять примененную фильтрацию при переходе на новую страницу
# True сообщает Django, что для работы тега требуется передать контекст
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    # Позволяет скопировать все параметры текущего запроса
    d = context['request'].GET.copy()
    # По указанным полям мы просто устанавливаем новые значения, которые нам передали при использовании тега
    for k, v in kwargs.items():
        d[k] = v
    # Кодируем параметры в формат, который может быть указан в строке браузера,
    # т.к. не каждый символ разрешается использовать в пути и параметрах запроса
    return d.urlencode()