from django import template

register = template.Library()

# Create your own template tags here.
# Example:
#@register.simple_tag
#def add(x, y):
#  return x + y


@register.filter
def score(attempt):
  return str(attempt.score * 100) + '%'


@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)
