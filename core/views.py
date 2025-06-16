import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import TelegramUser
from django.conf import settings
import json

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

            TelegramUser.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )

        return JsonResponse({"status": "received"})

    return JsonResponse({"error": "Invalid request"}, status=400)
