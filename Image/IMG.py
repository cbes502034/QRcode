import io
import base64
import qrcode
def src(URI):
    img_io = io.BytesIO()
    img = qrcode.make(URI)
    img.save(img_io, format='PNG')
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.read()).decode('utf-8')
    img_data_uri = f"data:image/png;base64,{base64_img}"
    return img_data_uri
