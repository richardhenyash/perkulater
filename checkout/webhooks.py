# Stripe webhook code referenced from:
# https://stripe.com/docs/payments/handling-payment-events

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import stripe
from checkout.webhook_handler import Stripe_WebHook_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup stripe keys
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Construct webhook events
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(content=e, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(content=e, status=400)
    except Exception as e:
        # Generic error
        return HttpResponse(content=e, status=400)

    # Set up a webhook handler
    handler = Stripe_WebHook_Handler(request)

    # Map webhook events to the relevant handler functions
    ps = handler.handle_payment_intent_succeeded
    pf = handler.handle_payment_intent_payment_failed
    event_map = {
        'payment_intent.succeeded': ps,
        'payment_intent.payment_failed': pf,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
