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