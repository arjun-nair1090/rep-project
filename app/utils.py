from threading import Thread
from barcode import EAN13
from random import randint
from .models import *
from barcode.writer import ImageWriter
from django.conf import settings
import os
from django.conf import settings
from django.core.mail import EmailMessage
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from zipfile import ZipFile
import csv


class EmailThread(Thread):
    def __init__(self, subject, body, email, attachments=None):
        self.subject = subject
        self.body = body
        self.email = email
        self.attachments = attachments
        Thread.__init__(self)

    def run(self):
        from_email = "djangodeveloper09@gmail.com"
        to = self.email

        if isinstance(to, str):
            e = EmailMessage(self.subject, self.body, from_email, [to])
        else:
            e = EmailMessage(self.subject, self.body, from_email, to)

        if self.attachments is not None:
            e.attach_file(self.attachments)
        e.send()


class GenerateBRCode(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sku_list = SKUItems.objects.all()

        for sku in sku_list:

            try:

                if sku.sku_barcode_image:
                    pass
            except Exception as ep:

                filename = f"{sku.sku_serial_no}.jpg"
                filepath = f"/media/barcode/{filename}"

                with open(filepath, "wb") as f:
                    EAN13(sku.sku_serial_no, writer=ImageWriter()).write(f)

                sku.sku_barcode_image = filepath

                sku.save()


def generate_BRC():
    sku_list = SKUItems.objects.all()

    for sku in sku_list:
        filepath = "{}.jpg".format(sku.sku_serial_no)

        sku.sku_barcode_image = os.path.join(settings.MEDIA_ROOT, filepath)
        sku.save()


def generate_barcode(sno=None):
    if sno is None:
        sno = EAN13(str(randint(100000000000, 999999999999)), writer=ImageWriter())

    filename = "{}.jpg".format(sno)
    filepath = "./media/barcode/{}".format(filename)

    with open(filepath, "wb") as f:
        EAN13(sno, writer=ImageWriter()).write(f)

    return filename


## Logic Incomplete @
def zipBarcodes():
    sku_file_paths = SKUItems.objects.all().values_list("sku_barcode_image", flat=True)
    with ZipFile("./media/AllBarcodes.zip", "w") as archive:
        for image_path in sku_file_paths:
            if image_path == "backup/":
                continue
            elif image_path is not None:
                archive.write(
                    os.path.join(settings.MEDIA_ROOT, image_path),
                    arcname=os.path.basename(image_path),
                )


def sendEmailReport():
    """send email to every user in database"""

    user_email = "djangodeveloper09@gmail.com"

    today_date = date.today().strftime("%Y-%m-%d")

    bypass_sku_data = ByPassModel.objects.filter(bypass_date=today_date)

    try:
        if bypass_sku_data.exists():
            with open("BypassData.csv", mode="w") as employee_file:
                writer = csv.writer(employee_file)
                writer.writerow(
                    [
                        "Invoice_no",
                        "Bypass S.K.U. Name",
                        "Bypass Against S.K.U. Name",
                        "Bypass Date",
                        "Bypass Time",
                    ]
                )

                bypass_data = ByPassModel.objects.filter(
                    bypass_date=today_date
                ).values()
                for each in bypass_data:

                    invoice_no = Invoice.objects.get(
                        id=each["bypass_invoice_no_id"]
                    ).invoice_no
                    bypass_sku_name = SKUItems.objects.get(
                        id=each["bypass_sku_name_id"]
                    ).sku_name
                    bypass_against_sku_name = SKUItems.objects.get(
                        id=each["bypass_against_sku_name_id"]
                    )
                    bypass_date = each["bypass_date"].strftime("%Y-%m-%d")
                    bypass_time = each["bypass_time"].strftime("%H:%M:%S %p")

                    bypass_data = (
                        invoice_no,
                        bypass_sku_name,
                        bypass_against_sku_name,
                        bypass_date,
                        bypass_time,
                    )
                    writer.writerow(bypass_data)

            EmailThread(
                "Bypass SKU List CSV data",
                "CSV file for Bypass SKU Items",
                [user_email],
                attachments="BypassData.csv",
            ).start()
        else:
            EmailThread(
                "Bypass SKU List CSV data",
                "There is no bypass SKU List generated today",
                [user_email],
            ).start()
    except Exception as e:
        print("Error in sendEmailReport -> ", e)


def startSchedular():
    """Create a BackgroundScheduler, and set the daemon parameter to True.
    This allows us to kill the thread when we exit the DJANGO application."""
    try:
        schedular = BackgroundScheduler(deamon=True)
        schedular.add_job(sendEmailReport, "cron", hour=1, minute=1)
        schedular.start()
    except Exception as e:
        print("schedular shutdown successfully")
        schedular.shutdown()


def mapBaseQty(filename="sku.csv"):
    """Map data from CSV file -> SKU Name and update SKU base qty"""
    with open(os.path.join(filename)) as csvfile:
        csvreader = csv.DictReader(csvfile)

        for i in csvreader:
            sku_item = i["ITEM"]
            is_sku = SKUItems.objects.filter(sku_name=sku_item)
            if is_sku.exists():
                fetch_sku = SKUItems.objects.get(sku_name=sku_item)
                fetch_sku.sku_base_qty = 1 if i["PACKING"] == "" else i["PACKING"]
                fetch_sku.save()