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

def generate_email_body_new_article_version(user_email, article_title, new_version_title):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
        <div style="background-color: #28a745; color: white; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">A New Version of Your Article Has Been Created!</h1>
        <p style="margin: 10px 0;">Your article has been updated with a new version created by <strong>{user_email}</strong>.</p>
        </div>
        
        <div style="padding: 20px; background-color: #ffffff;">
        <h2 style="color: #28a745;">Article Details</h2>
        <p><strong>Article Title:</strong> <em>{article_title}</em></p>
        <p><strong>New Version Title:</strong> <em>{new_version_title}</em></p>
        <p><strong>Summary of Changes:</strong> A new version of your article has been created. Please review the latest changes to ensure they align with your expectations.</p>
        </div>
    </body>
    </html>
    """

def generate_email_body_deletion_article(user_email, article_title):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
        <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">Your Article Has Been Deleted!</h1>
        <p style="margin: 10px 0;">The user with email <strong>{user_email}</strong> has deleted one of your articles.</p>
        </div>
        
        <div style="padding: 20px; background-color: #ffffff;">
        <h2 style="color: #dc3545;">Deletion Details</h2>
        <p><strong>Deleted Article:</strong> <em>{article_title}</em></p>
        </div>
    </body>
    </html>
    """

def generate_email_body_version_deleted(user_email, article_version_title):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
        <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">Your Article Version Has Been Deleted!</h1>
        <p style="margin: 10px 0;">The user with email <strong>{user_email}</strong> has deleted your article version.</p>
        </div>
        
        <div style="padding: 20px; background-color: #ffffff;">
        <h2 style="color: #dc3545;">Deletion Details</h2>
        <p><strong>Deleted Article Version:</strong> <em>{article_version_title}</em></p>
        </div>
    </body>
    </html>
    """

def generate_email_body_version_deleted_author(user_email, article_title, article_version_title):
    return f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
            <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">A Version of Your Article Has Been Deleted!</h1>
                <p style="margin: 10px 0;">The user with email <strong>{user_email}</strong> has deleted a version of your article.</p>
            </div>
            
            <div style="padding: 20px; background-color: #ffffff;">
                <h2 style="color: #dc3545;">Deletion Details</h2>
                <p><strong>Article Title:</strong> <em>{article_title}</em></p>
                <p><strong>Deleted Version Title:</strong> <em>{article_version_title}</em></p>
            </div>
        </body>
        </html>
        """

def generate_email_body_restore_version(user_email, restored_version_title, restored_version_author):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0;">
        <div style="background-color: #ffc107; color: white; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">Your Article Has Been Restored!</h1>
        <p style="margin: 10px 0;">The user with email <strong>{user_email}</strong> has restored an older version of your article.</p>
        </div>
        
        <div style="padding: 20px; background-color: #ffffff;">
        <h2 style="color: #ffc107;">Restoration Details</h2>
        <p><strong>Restored Article Version:</strong> <em>{restored_version_title}</em></p>
        <p><strong>Restored Article Version Author:</strong> <em>{restored_version_author}</em></p>
        <p>Please review the restored content to ensure it meets your expectations.</p>
        </div>
    </body>
    </html>
    """


