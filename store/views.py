from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, DigitalProduct, CartItem, Order, OrderItem, PurchasedProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import CartItem, Order, OrderItem, Payment
from .utils import process_mpesa_payment, process_paypal_payment, process_stripe_payment
from .utils import send_payment_confirmation_email
import stripe
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment


def product_list(request):
    """Show all books & audiobooks"""
    categories = Category.objects.all()
    products = stripe.Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    """Show product details with preview (but restrict full access)"""
    product = get_object_or_404(stripe.Product, id=product_id)
    
    # Check if user already purchased the book
    has_access = product.is_purchased_by(request.user) if request.user.is_authenticated else False

    return render(request, 'store/product_detail.html', {'product': product, 'has_access': has_access})


def product_detail(request, product_id):
    """View individual e-book/audiobook details."""
    product = get_object_or_404(DigitalProduct, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    """Add a product to the shopping cart."""
    product = get_object_or_404(DigitalProduct, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, "Product added to cart.")
    return redirect('cart')


@login_required
def cart_view(request):
    """Display all items in the user's cart."""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    """Process checkout and create an order."""
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price, status='pending')

    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
        PurchasedProduct.objects.create(user=request.user, product=item.product)  # Give user access
    
    cart_items.delete()  # Clear cart after checkout
    messages.success(request, "Order placed successfully!")
    return redirect('order_history')



@login_required
def initiate_payment(request):
    """Handles payment initiation for different payment methods."""
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price, status='pending')

        # Save ordered items
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)

        # Clear cart
        cart_items.delete()

        # Create a Payment instance
        payment = Payment.objects.create(user=request.user, order=order, amount=total_price, method=payment_method, status='pending')

        # Redirect to the appropriate payment gateway
        if payment_method == 'mpesa':
            return process_mpesa_payment(request, payment)
        elif payment_method == 'paypal':
            return process_paypal_payment(request, payment)
        elif payment_method == 'stripe':
            return process_stripe_payment(request, payment)

        messages.error(request, "Invalid payment method.")
        return redirect('checkout')

    return render(request, 'store/checkout.html')


@csrf_exempt
def mpesa_webhook(request):
    """Handle M-Pesa payment notifications."""
    data = json.loads(request.body.decode('utf-8'))
    transaction_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
    result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')

    try:
        payment = Payment.objects.get(transaction_id=transaction_id)

        if result_code == 0:  # Success
            payment.status = 'completed'
            payment.is_downloadable = True  # Enable downloads
            payment.webhook_data = data
            payment.save()

            # Send email confirmation
            send_payment_confirmation_email(payment.user, payment.order)

        else:  # Failed
            payment.status = 'failed'
            payment.webhook_data = data
            payment.save()

    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=400)

    return JsonResponse({'message': 'Webhook received successfully'})

@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal payment webhook notifications."""
    data = json.loads(request.body.decode('utf-8'))
    event_type = data.get('event_type')

    if event_type == "CHECKOUT.ORDER.APPROVED":
        transaction_id = data.get('resource', {}).get('id')
        payer_email = data.get('resource', {}).get('payer', {}).get('email_address', '')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)

            # Mark payment as completed
            payment.status = 'completed'
            payment.is_downloadable = True  # Enable downloads
            payment.webhook_data = data
            payment.save()

            # Send confirmation email
            send_payment_confirmation_email(payment.user, payment.order)

        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=400)

    return JsonResponse({'message': 'PayPal webhook received successfully'})


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe payment webhook notifications."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        transaction_id = session['id']
        customer_email = session.get('customer_email', '')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)

            # Mark payment as completed
            payment.status = 'completed'
            payment.is_downloadable = True  # Enable downloads
            payment.webhook_data = event['data']
            payment.save()

            # Send confirmation email
            send_payment_confirmation_email(payment.user, payment.order)

        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=400)

    return JsonResponse({'message': 'Stripe webhook received successfully'})


@login_required
def download_purchases(request):
    """Allow users to download their purchased items after successful payment."""
    user_payments = Payment.objects.filter(user=request.user, status="completed", is_downloadable=True)
    
    return render(request, 'store/downloads.html', {'purchases': user_payments})

