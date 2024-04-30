from django import template

register = template.Library()

stop_word = [
    'украина',
    'украине',
]

@register.filter(name = 'censor')
def censor(value):
    text = value.split()
    for sw in stop_word:
        for id, word in enumerate(text):
            if word.lower() == sw:
                text[id] = word[0] + '*' * (len(word) - 1)

    return ' '.join(text)


