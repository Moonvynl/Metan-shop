import random
import urllib.request
import os
from django.core.files.base import ContentFile
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


avatars = [
    "/default_avatar1.png",
    "/default_avatar2.png",
    "/default_avatar3.png",
    "/default_avatar4.png",
    "/default_avatar5.png",
    "/default_avatar6.png",
    "/default_avatar7.png",
]

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        google_avatar_url = None

        if sociallogin.account.provider == "google":
            google_avatar_url = sociallogin.account.extra_data.get("picture")

        if google_avatar_url:
            try:
                result = urllib.request.urlopen(google_avatar_url)
                user.avatar.save(
                    f"avatars/{user.username}_google.jpg",
                    ContentFile(result.read()),
                    save=True,
                )
            except Exception as e:
                print(f"Помилка завантаження аватара: {e}")
                user.avatar = random.choice(avatars)
        else:
            user.avatar = random.choice(avatars)

        user.save()
        return user