from io import BytesIO
from django.core.files import File

import qrcode


def generate_qr_code(ticket_info: str) -> File:
    """
       Generates a QR code for the provided information and returns a file object.

       Parameters:
       ticket_info (str): Information to be embedded in the QR code.

       Returns:
       File: A file object containing the QR code in PNG format.
       """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket_info)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    temp_handle = BytesIO()
    img.save(temp_handle, format='png')
    temp_handle.seek(0)

    return File(temp_handle)
