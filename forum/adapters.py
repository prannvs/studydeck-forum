from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.shortcuts import redirect
from allauth.core.exceptions import ImmediateHttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if not sociallogin.user.email:
             return
             
        email = sociallogin.user.email
        
        allowed_domains = ['bits-pilani.ac.in', 'pilani.bits-pilani.ac.in'] 
        
        try:
            domain = email.split('@')[1]
        except IndexError:
            messages.error(request, "Invalid email address.")
            raise ImmediateHttpResponse(redirect('account_login'))

        if not any(domain.endswith(d) for d in allowed_domains):
            messages.error(request, f"Access Denied: The email '{email}' is not a BITS Pilani address.")
            raise ImmediateHttpResponse(redirect('account_login'))