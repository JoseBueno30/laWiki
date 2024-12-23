import yagmail

def enviar_email(destinatario, asunto, cuerpo):
    email_usuario = " lawikiwebapp@gmail.com"
    email_contraseña = "qbfx molx sokm rccz"

    try:
        yag = yagmail.SMTP(email_usuario, email_contraseña)

        yag.send(to=destinatario, subject=asunto, contents=cuerpo)
        print("Correo enviado correctamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

#enviar_email("ezesanchezgarcia@gmail.com", "Asunto de prueba", "Este es un correo de prueba.")
