from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_status_notification(email,job_title,new_status):
    subject = f"Update on your job application for {job_title}"
    from_email = 'katouahaneen@gmail.com'  
    to = [email]

    
    text_content = f"Hello,\n\nYour job application for '{job_title}' has been updated to: {new_status}.\n\nBest regards,\nJob Portal Team"

    
    status_colors = {
        "accepted": "#28B463",      # أخضر
        "under_review": "#2980B9",  # أزرق
        "rejected": "#C0392B"       # أحمر
    }
    color = status_colors.get(new_status, "#000000")  


    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2E86C1;">Job Portal Notification</h2>
        <p>Hello,</p>
        <p>Your job application for <strong>{job_title}</strong> has been updated to:</p>
        <h3 style="color: {color};">{new_status.upper()}</h3>
        <p>Best regards,<br>Job Portal Team</p>
      </body>
    </html>
    """

   
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)