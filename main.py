from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
import stripe
from flask_login import login_user, UserMixin, LoginManager, current_user, logout_user
import time
import os

PUB_KEY = os.environ.get("PUB_KEY")
stripe.api_key = os.environ.get("STRIPE_API")

# https://colorhunt.co/palette/040d12183d3d5c837493b1a6

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///ceramics.db')
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

shopping_cart = []
domain_url = "http://127.0.0.1:5000/"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250))
    stripe_id = db.Column(db.String(250), unique=True)
    active = db.Column(db.Boolean)
    price = db.Column(db.Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


def add_product(name, img_url, price_amount):
    new_product = stripe.Product.create(name=name, images=[img_url])
    stripe.Price.create(currency="usd", unit_amount=price_amount, product=new_product.stripe_id)
    with app.app_context():
        db_product = Product(name=name, img_url=img_url, stripe_id=new_product.id, active=True, price=price_amount)
        db.session.add(db_product)
        db.session.commit()


new_items = [["Lotus Bowl", "ctk001.jpeg", 5000],
             ["Royal Blue Bowl", "ctk002.jpeg", 3000],
             ["Sunshine in Eggshell", "ctk003.jpeg", 3500],
             ["Small 'Stitched' Vase", "ctk004.jpeg", 3000],
             ["Tree Vase", "ctk005.jpeg", 5000],
             ["Royal Blue Tray", "ctk006.jpeg", 3000],
             ["Sea-green Pot with Lid", "ctk007.jpeg", 4000],
             ["Tree Roots Pot with Lid", "ctk008.jpeg", 4500]]

# for item in new_items:
#     add_product(item[0], item[1], item[2])


def create_session(list_items):
    line_items = [{"price": item["price_id"], "quantity": 1} for item in list_items]

    new_session = stripe.checkout.Session.create(
            success_url=domain_url + "success",
            cancel_url=domain_url + "cancel",
            line_items=line_items,
            mode="payment",
            customer_email="sample@gmail.com",
            expires_at=int(time.time()) + 3600)
    return new_session


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/paintings')
def paintings():
    return render_template('paintings.html')


@app.route('/shop')
def shop():
    results = db.session.execute(db.select(Product).where(Product.active))
    all_products = results.scalars()
    product_list = [product.to_dict() for product in all_products]
    return render_template('shop.html', products=product_list)


@app.route('/add/<product_id>')
def add_to_cart(product_id):
    shopping_cart.append(product_id)
    product = db.session.execute(db.select(Product).where(Product.stripe_id == product_id)).scalar()
    flash(f"The item '{product.name}' has been added to the shopping cart.")
    return redirect(url_for('shop'))


@app.route('/remove/<product_id>')
def remove_from_cart(product_id):
    shopping_cart.remove(product_id)
    product = db.session.execute(db.select(Product).where(Product.stripe_id == product_id)).scalar()
    flash(f"The item '{product.name}' has been removed from the shopping cart.")
    return redirect(url_for('cart'))


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_account = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user_account:
            hashed_password = user_account.password
            if check_password_hash(pwhash=hashed_password, password=password):
                login_user(user_account)
                return redirect(url_for('home'))
            else:
                flash("The password is incorrect. Please try again.")
                return redirect(url_for('login'))
        else:
            flash("This account doesn't exist, please register instead.")
            return redirect(url_for('register'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        hashed_password = generate_password_hash(
            password=form.password.data,
            method="pbkdf2:sha256",
            salt_length=8)
        new_user = User(name=name, email=email, password=hashed_password)
        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("That account already exists. Please login instead.")
            return redirect(url_for('login'))
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/cart')
def cart():
    prelim_list = []
    for item in shopping_cart:
        product = db.session.execute(db.select(Product).where(Product.stripe_id == item)).scalar()
        prelim_list.append(product)

    product_list = [product.to_dict() for product in prelim_list]

    return render_template('checkout.html', cart=product_list)


@app.route('/checkout-session')
def checkout_session():
    checkout_list = []
    for product_id in shopping_cart:
        price_id = stripe.Price.list(product=product_id)["data"][0]["id"]
        price = stripe.Price.list(product=product_id)["data"][0]["unit_amount"]
        item_details = {"product_id": product_id, "price_id": price_id, "price": price}
        checkout_list.append(item_details)

    # create checkout session
    s = create_session(checkout_list)
    # print(s)
    return redirect(s["url"])


@app.route('/success')
def success():
    global shopping_cart
    shopping_cart = []
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


if __name__ == "__main__":
    app.run(debug=True)
