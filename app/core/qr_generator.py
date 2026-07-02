import os 
import qrcode


def generate_qrcode(
        gatepass_id:str
):
    os.makedirs(
    "app/static/qr_codes",
    exist_ok=True
    )

    filepath = (
        f"app/static/qr_codes/{gatepass_id}.png"
    )
    
    img =qrcode.make(
        gatepass_id
    )

    img.save(
        filepath
    )

    return f"qr_codes/{gatepass_id}.png"