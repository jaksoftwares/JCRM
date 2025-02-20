from django.shortcuts import render, redirect
from django.contrib import messages
import paypalrestsdk
from .models import Donation
from .forms import DonationForm
import requests
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Donation
from .forms import DonationForm
import stripe
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment


# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Configure PayPal environment
if settings.PAYPAL_MODE == "sandbox":
    paypal_env = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
else:
    paypal_env = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)

paypal_client = PayPalHttpClient(paypal_env)

def donate(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.user = request.user  # Link to logged-in user
            
            payment_method = request.POST.get("payment_method")
            
            if payment_method == "stripe":
                try:
                    charge = stripe.Charge.create(
                        amount=int(donation.amount * 100),  # Convert to cents
                        currency=donation.currency.lower(),
                        description=f"Donation to JCRM - {donation.amount} {donation.currency}",
                        source=request.POST["stripeToken"]
                    )
                    donation.status = "Completed"
                    donation.transaction_id = charge.id
                except stripe.error.StripeError as e:
                    messages.error(request, f"Stripe Payment Failed: {e}")
                    return redirect("donations:donate")

            elif payment_method == "paypal":
                request_order = OrdersCreateRequest()
                request_order.prefer("return=representation")
                request_order.request_body({
                    "intent": "CAPTURE",
                    "purchase_units": [{
                        "amount": {
                            "currency_code": donation.currency.upper(),
                            "value": f"{donation.amount:.2f}"
                        },
                        "description": f"Donation to JCRM - {donation.amount} {donation.currency}"
                    }]
                })
                
                try:
                    response = paypal_client.execute(request_order)
                    approval_url = next(link.href for link in response.result.links if link.rel == "approve")
                    donation.status = "Pending"
                    donation.transaction_id = response.result.id
                    donation.save()
                    return redirect(approval_url)
                except Exception as e:
                    messages.error(request, f"PayPal Payment Failed: {e}")
                    return redirect("donations:donate")

            donation.save()
            messages.success(request, "Your donation has been received. Thank you!")
            return redirect("donations:donation_success")
    
    else:
        form = DonationForm()

    return render(request, "donations/donate.html", {"form": form, "stripe_key": settings.STRIPE_PUBLIC_KEY})



def donation_success(request):
    """
    Displays a thank-you page after a successful donation.
    """
    return render(request, "donations/donation_success.html")

@login_required
def donation_history(request):
    """
    Shows the donation history of a logged-in user.
    """
    donations = Donation.objects.filter(user=request.user).order_by("-date")
    return render(request, "donations/donation_history.html", {"donations": donations})

@login_required
def donation_detail(request, donation_id):
    """
    Displays details of a specific donation.
    """
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    return render(request, "donations/donation_detail.html", {"donation": donation})


       # Mpesa

def process_mpesa_payment(phone_number, amount):
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {settings.MPESA_ACCESS_TOKEN}"}
    
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": settings.MPESA_PASSWORD,
        "Timestamp": "20250218120000",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "JCRM Donations",
        "TransactionDesc": "Church Donation"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# Initialize PayPal Client
def get_paypal_client():
    environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET) if settings.PAYPAL_MODE == "sandbox" else LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
    return PayPalHttpClient(environment)

def paypal_success(request):
    """
    Handles successful PayPal donations using the new PayPal Checkout SDK.
    """
    order_id = request.GET.get("paymentId")  # PayPal's order ID
    payer_id = request.GET.get("PayerID")  # Not needed in new SDK, but captured for reference

    if not order_id:
        messages.error(request, "Invalid PayPal transaction.")
        return redirect("donations:donate")

    client = get_paypal_client()
    capture_request = OrdersCaptureRequest(order_id)

    try:
        response = client.execute(capture_request)
        if response.status_code == 201:
            # Get the transaction ID from PayPal response
            transaction_id = response.result.id

            # Update the donation record in the database
            donation = Donation.objects.get(transaction_id=order_id)
            donation.status = "Completed"
            donation.save()

            messages.success(request, "Your PayPal donation was successful!")
            return redirect("donations:donation_success")
        else:
            messages.error(request, "PayPal transaction could not be completed.")
    except Exception as e:
        messages.error(request, f"PayPal transaction failed: {str(e)}")

    return redirect("donations:donate")



