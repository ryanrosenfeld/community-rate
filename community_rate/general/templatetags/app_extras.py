from django import template
register = template.Library()


@register.inclusion_tag('navbar_og.html')
def show_results(poll):
    choices = poll.choice_set.all()
    return {'choices': choices}