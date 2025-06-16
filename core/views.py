import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import TelegramUser
from .tasks import send_welcome_email

# Public endpoint
@api_view(["GET"])
@permission_classes([AllowAny])
def public_view(request):
    return Response({"message": "This is a public endpoint. Anyone can access it!"})


# Protected endpoint (JWT required)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    return Response({"message": f"Hello, {user.username}! You are authenticated."})


# User registration + Celery email
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if not username or not password or not email:
        return Response({"error": "Username, password, and email are required."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)

    # Trigger Celery welcome email
    send_welcome_email.delay(user.email)

    return Response({"message": "User registered successfully. Welcome email is being sent."})


# Telegram webhook handler
@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message", {})

        if message.get("text") == "/start":
            chat = message.get("from", {})
            telegram_id = chat.get("id")
            username = chat.get("username")
            first_name = chat.get("first_name")
            last_name = chat.get("last_name")
            print("✅ Telegram /start received from:", telegram_id, username, first_name, last_name)

            # Store or retrieve Telegram user
            user, created = TelegramUser.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )

            # Optional reply (uncomment to send message)
            # bot_token = settings.TELEGRAM_BOT_TOKEN
            # welcome_text = f"Welcome, {first_name or 'there'}!"
            # requests.post(
            #     f"https://api.telegram.org/bot{bot_token}/sendMessage",
            #     json={"chat_id": telegram_id, "text": welcome_text}
            # )

        return JsonResponse({"status": "received"})

    return JsonResponse({"error": "Invalid request method"}, status=400)
