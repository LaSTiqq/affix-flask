from flask import Flask, render_template, flash, redirect, url_for, request, make_response, Response
from flask_wtf.csrf import CSRFProtect
from flask_mail import Message, Mail
from flask_static_digest import FlaskStaticDigest
from flask_talisman import Talisman
from config import Config
from utils import restricted_list, year_and_month
from forms import ContactForm
import re
import os

flask_static_digest = FlaskStaticDigest()

app = Flask(__name__)
app.config.from_object(Config)

flask_static_digest.init_app(app)

app.secret_key = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

talisman = Talisman(app, content_security_policy=None, force_https=False)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv("RECAPTCHA_PRIVATE_KEY")
app.config['RECAPTCHA_PARAMETERS'] = {'hl': 'lv'}


@app.route("/", methods=["GET", "POST"])
def index():
    current_month, current_year = year_and_month()
    cookie_accepted = request.cookies.get("cookie_accepted") == "true"
    form = ContactForm()
    if form.validate_on_submit():
        if any(restricted_list(form[field].data) for field in ['name', 'subject', 'message']):
            flash("Jūs ievadījāt kaut ko aizliegtu! Mēģiniet vēlreiz.", "warning")
            return redirect(url_for("index") + "#contact_us")
        html_content = render_template("email.html", name=form.name.data,
                                       sender=form.email.data, content=form.message.data)
        text_content = re.sub(r"<[^>]+>", "", html_content)
        try:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=['lavrencij@inbox.lv'],
                body=text_content
            )
            msg.html = html_content
            mail.send(msg)
            flash("Vēstule nosūtīta!", "success")
            return redirect(url_for("index") + "#contact_us")
        except Exception:
            flash("Kaut kas nogāja greizi! Mēģiniet vēlreiz.", "danger")
            return redirect(url_for("index") + "#contact_us")
    if form.errors:
        if 'recaptcha' in form.errors:
            flash("Captcha netika izpildīta! Mēģiniet vēlreiz.", "warning")
        return redirect(url_for("index") + "#contact_us")
    return render_template('index.html', form=form, current_month=current_month, current_year=current_year, cookie_accepted=cookie_accepted)


@app.route("/accept-cookies", methods=["POST"])
def accept_cookies():
    response = make_response("Cookie Accepted")
    response.set_cookie("cookie_accepted", "true",
                        max_age=31536000, secure=True)
    return response


@app.route('/sitemap.xml')
def sitemap_xml():
    content = render_template('crawlers/sitemap.xml')
    return Response(content, mimetype='application/xml')


@app.route('/robots.txt')
def robots_txt():
    content = render_template('crawlers/robots.txt')
    return Response(content, mimetype='text/plain')
