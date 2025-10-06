# import random
# from django.core.mail import send_mail
#
# def generate_otp():
#     return str(random.randint(100000, 999999))
#
# def send_otp_email(user_email, otp):
#     send_mail(
#         'Tasdiqlash kodi',
#         f'Sizning tasdiqlash kodingiz: {otp}',
#         'noreply@uzummarket.uz',
#         [user_email],
#         fail_silently=False,
#     )
