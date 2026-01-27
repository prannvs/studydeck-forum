from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        allowed_domains = ['bits-pilani.ac.in', 'pilani.bits-pilani.ac.in'] 
        domain = email.split('@')[1]
        if not any(domain.endswith(d) for d in allowed_domains):
            raise ValidationError("Only BITS Pilani email addresses are allowed.")