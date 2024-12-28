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

def generate_email_body_new_comment(user_email, article_name, new_comment):
    return f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #66b2ff; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0; color: white;">New Comment on Your Article!</h1>
            <p style="margin: 10px 0;">The user with email <strong>{user_email}</strong> has left a comment on one of your articles.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff; color: black;">
            <h2 style="color: #66b2ff;">Comment Details</h2>
            <p><strong>Commented Article:</strong> <em>{article_name}</em></p>
            <p><strong>Comment:</strong></p>
            <blockquote style="background-color: #f0f0f0; padding: 10px; border-left: 4px solid #66b2ff;">
                "{new_comment}"
            </blockquote>
            </div>
        </body>
        </html>
        """

