import stripe
import time
import webbrowser
import os

PUB_KEY = "pk_test_51Oqy87HhJRuuTnPGJie0G6UTo0I274OrCqCzJpRKw8QAHO5mL6c4mNV7sK60Fj4dA2fr8PNThzbZe1c9RYy5B0qP00GsMASYRG"
stripe.api_key = "sk_test_51Oqy87HhJRuuTnPG9amU2QoI6ni8dPZBXI4A4li5Hyu3Y357ksIc3A3mh4cWcxogb8iEIenvini1tobNXps5YmZU00JHMBObwJ"

success_url = "http://www.example.com/success"
cancel_url = "http://www.example.com/cancel"
# create a customer object

# create a checkout session
def create_session(price):
    new_session = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            line_items=[{"price": price, "quantity": 1}],
            mode="payment",
            customer_email="sample@gmail.com",
            expires_at=int(time.time()) + 3600)
    return new_session

# for product in stripe.Product.list()["data"]:
#     stripe.Product.modify(product.id, active=False)


# product_id = stripe.Product.list(active=True)["data"][0]["id"]
# price_id = stripe.Price.list(product=product_id)["data"][0]["id"]
# print(stripe.Price.list(product=product_id)["data"][0]["unit_amount"])
#
# s = create_session(price_id)
# print(s)
#
# session_id = s["id"]
# webbrowser.open(s["url"])
# input("press enter to continue...")
# print(f"current session status: {stripe.checkout.Session.retrieve(session_id)['status']}")
# print(f"current payment status: {stripe.checkout.Session.retrieve(session_id)['payment_status']}")
customer = stripe.Customer.create(name="Yvonne Wang", email="susanlearnspython@gmail.com")
print(customer["id"])
customer_get = stripe.Customer.retrieve(customer["id"])




