from django.contrib.auth.decorators import login_required

from profiles.models import SocialProfiles


def profile_info(user):
    return {
        'name': user.name(),
        'username': user.username,
        'first_name': user.first_name,
        'area': user.area,
        'email': user.email,
        'phone': user.phone,
        'status': user.status
    }


def social_info(user):
    try:
        social = SocialProfiles.objects.get(user=user)
    except SocialProfiles.DoesNotExist:
        return {}
    return {
        'blog': social.blog,
        'twitter': social.twitter,
        'linkedin': social.linkedin,
        'facebook': social.facebook,
        'instagram': social.instagram,
        'portfolio': social.portfolio
    }
