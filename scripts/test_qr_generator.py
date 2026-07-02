from app.core.qr_generator import generate_qrcode


path=generate_qrcode(
    "TEST_GATEPASS"
)

print (path)