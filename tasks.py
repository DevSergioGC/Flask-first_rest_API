import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader) 

#* Function that gets all the variables that we'll need to render the template (in case we have)
def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Sergio Guzmán <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html
        }
    )

def send_user_registration_email(email, username):
    return send_simple_message(
        to = email,
        subject = "Successfully signed up",
        body = f"Hi {username}! You have successfully signed up to the Stores REST API.",
        html = render_template("email/action.html", username=username)
    )