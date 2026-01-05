from django import template
from allauth.socialaccount.models import SocialAccount

register = template.Library()

@register.filter
def google_avatar(user):
    try:
        social = SocialAccount.objects.filter(user=user, provider='google').first()
        if social and 'picture' in social.extra_data:
            return social.extra_data['picture']
    except Exception:
        pass
    return "https://ui-avatars.com/api/?name=" + user.username

@register.filter
def get_item(queryset, key):
    """
    Look up an item in a QuerySet by its ID.
    Usage: {{ categories|get_item:current_category_id }}
    """
    try:
        return queryset.get(id=key).name
    except:
        return ""