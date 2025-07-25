from flask import Flask, render_template, make_response, Response, request, jsonify
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_mail import Message, Mail
from config import Config
from utils import restricted_list, year_and_month
from forms import ContactForm
import re

flask_static_digest = FlaskStaticDigest()

app = Flask(__name__)
app.config.from_object(Config)

flask_static_digest.init_app(app)
csrf = CSRFProtect(app)
talisman = Talisman(app, content_security_policy=None, force_https=False)
mail = Mail(app)


@app.route("/", methods=["GET"])
def index():
    current_month, current_year = year_and_month()
    cookie_accepted = request.cookies.get("cookie_accepted") == "true"
    form = ContactForm()
    return render_template('index.html', form=form, current_month=current_month, current_year=current_year, cookie_accepted=cookie_accepted)


@app.route("/send-ajax", methods=["POST"])
def send_ajax():
    form = ContactForm()
    if form.validate_on_submit():
        if any(restricted_list(form[field].data) for field in ['name', 'subject', 'message']):
            return jsonify({"status": "warning", "message": "Jūs ievadījāt kaut ko aizliegtu! Lūdzu, mēģiniet vēlreiz."}), 400
        html_content = render_template("email.html", name=form.name.data,
                                       email=form.email.data, message=form.message.data)
        text_content = re.sub(r"<[^>]+>", "", html_content)
        try:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=['affixsia@inbox.lv'],
                body=text_content
            )
            msg.html = html_content
            mail.send(msg)
            return jsonify({"status": "success", "message": "Vēstule nosūtīta!"})
        except Exception:
            return jsonify({"status": "danger", "message": "Kaut kas nogāja greizi! Lūdzu, mēģiniet vēlreiz."}), 500
    else:
        return jsonify({"status": "warning", "message": "Captcha netika izpildīta! Lūdzu, mēģiniet vēlreiz."}), 400


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "error.html",
        error_code=404,
        error_message="Page Not Found",
        error_comment="Jūs esat nokļuvis uz neeksistējošu lapu."
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        "error.html",
        error_code=500,
        error_message="Internal Server Error",
        error_comment="Radās kļūda un serveris nespēja izpildīt Jūsu pieprasījumu."
    ), 500
