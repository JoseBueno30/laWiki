import yagmail

def send_email(recipient, subject, body_html):
    email_usuario = "lawikiwebapp@gmail.com"
    email_contraseña = "qbfx molx sokm rccz"

    try:
        yag = yagmail.SMTP(email_usuario, email_contraseña)

        yag.send(to=recipient, subject=subject, contents=body_html)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error while sending email: {e}")

