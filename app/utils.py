from threading import Thread
from django.core.mail import send_mail
# from .models import StockBarcode


class EmailThread(Thread):
    def __init__(self, email, otp):
        self.email = email
        self.otp = otp
        Thread.__init__(self)

    def run(self):
        from_email = "djangodeveloper09@gmail.com"
        to = self.email
        message = f"Please use the verification code below on the Doshi website: \n Your otp is {self.otp} \n If you didn't request this, you can ignore this email or let us know."
        send_mail("Hello", message, from_email, [to])

        
def generate():
    sno = EAN13(str(randint(100000000000, 999999999999))).ean
    if StockBarcode.objects.filter(serial_no=sno).count() > 0:
        generate()
    else:
        return sno
