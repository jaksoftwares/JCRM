from django.urls import reverse
import requests
from django.conf import settings
from django.shortcuts import redirect
from .models import Payment
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

M_PESA_BASE_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def process_mpesa_payment(request, payment):
    """Process M-Pesa STK Push"""
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": settings.MPESA_PASSKEY,
        "Timestamp": "20250219120000",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(payment.amount),
        "PartyA": request.user.profile.phone_number,  # User's phone number
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": request.user.profile.phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"Order-{payment.order.id}",
        "TransactionDesc": "Purchase of digital products"
    }
    
    headers = {"Authorization": f"Bearer {settings.MPESA_ACCESS_TOKEN}"}
    response = requests.post(M_PESA_BASE_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        payment.status = 'pending'
        payment.save()
        return redirect('order_history')

    payment.status = 'failed'
    payment.save()
    return redirect('checkout')


def process_paypal_payment(request, payment):
    """Redirect to PayPal Payment Gateway"""
    PAYPAL_URL = "https://www.paypal.com/checkoutnow"
    return redirect(f"{PAYPAL_URL}?amount={payment.amount}&order_id={payment.order.id}")


stripe.api_key = settings.STRIPE_SECRET_KEY

def process_stripe_payment(request, payment):
    """Generate Stripe Checkout Session"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Digital Product Purchase'},
                'unit_amount': int(payment.amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('order_history')),
        cancel_url=request.build_absolute_uri(reverse('checkout')),
    )

    return redirect(session.url)



def send_payment_confirmation_email(user, order):
    """Send email confirmation after successful payment."""
    subject = "Payment Successful - Download Your Purchase"
    message = f"""
    Hi {user.username},

    Your payment for Order #{order.id} has been successfully processed.
    
    You can now download your purchased items from your account.

    Visit: https://yourdomain.com/store/downloads/

    Thank you for shopping with us!
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

