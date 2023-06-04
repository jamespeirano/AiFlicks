import os
import stripe
from flask import jsonify

__all__ = ["checkout"]

stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def checkout(data):
    payment_method_id = data.get("paymentMethodId")
    amount = data.get("amount")
    try:
        payment_intent = stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            amount=amount,
            currency="usd",
            confirmation_method="manual",
            confirm=True,
        )
        if payment_intent.status == "succeeded":
            return jsonify({"success": True})

    except stripe.error.CardError as e:
        return jsonify({"success": False, "message": e.user_message})

    return jsonify({"success": False, "message": "Payment failed"})