import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def get_link(obj):
    if obj.paid_course:
        title = obj.paid_course.title
        description = obj.paid_course.description
    else:
        title = obj.paid_lesson.title
        description = obj.paid_lesson.description

    product = stripe.Product.create(
        name=title,
        description=description
    )
    product_price = stripe.Price.create(
        unit_amount=obj.amount * 90,
        currency='USD',
        product=product['id']
    )

    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payments/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
        line_items=[
            {
                'price': product_price,
                'quantity': 1
            }
        ],
        mode='payment',
        metadata={
            'payment_id': obj.id
        }
    )

    return session['url']
