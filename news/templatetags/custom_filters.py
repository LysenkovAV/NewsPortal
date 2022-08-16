from django import template


register = template.Library()

# список слов, которые цензурируются
BLACK_LIST = [
    'science',
    'space',
    'study',
]


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("This is not a string!")
    censored_text = text  # исходный текст
    text_list = text.split()  # получаем список слов исходного текста
    for i in text_list:
        if i.lower() in BLACK_LIST:  # если слово входит в черный список
            censored_text = censored_text.replace(i, i[0]+'*'*(len(i)-1))  # первую букву оставляем, остальные заменяем
    return censored_text
