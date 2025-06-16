import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Assuming your TelegramUser model is in the same app's models.py
# If it's in a different app, adjust the import accordingly (e.g., from myapp.models import TelegramUser)
from .models import TelegramUser


@api_view(["GET"])
@permission_classes([AllowAny])
def public_view(request):
    """
    A public endpoint that can be accessed by anyone.
    Demonstrates a simple Django REST Framework view.
    """
    return Response({"message": "This is a public endpoint. Anyone can access it!"})


@csrf_exempt
def telegram_webhook(request):
    """
    Handles incoming Telegram webhook updates.
    Specifically processes the "/start" command and saves user information.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message", {})

        if message.get("text") == "/start":
            chat = message.get("from", {})
            telegram_id = chat.get("id")
            username = chat.get("username")
            first_name = chat.get("first_name")
            last_name = chat.get("last_name")

            # Get or create the TelegramUser in your database
            user, created = TelegramUser.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )

        # Always return a 200 OK response to Telegram
        return JsonResponse({"status": "received"})

    # Return 400 for non-POST requests
    return JsonResponse({"error": "Invalid request method"}, status=400)
