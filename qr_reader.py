import PIL.ImageShow
from pylibdmtx import pylibdmtx
from PIL import Image

class QRReader:
    def read_qr_code(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        qr_roi = image.crop((0, 0, width, int(height * 0.3)))
        #PIL.ImageShow.show(qr_roi) # kırpılan kısmı gösterme satırı
        decoded_objects = pylibdmtx.decode(qr_roi)
        if decoded_objects:
            qr_code = decoded_objects[0].data.decode('utf-8')
            return self.process_qr_code(qr_code)
        return None

    def process_qr_code(self, qr_code):
        # KKB ve sonraki 5 karakteri ve sondaki 7 karakteri sil
        qr_code = qr_code.replace('KKB', '')[6:]
        # Son 7 karakteri sil
        qr_code = qr_code[:-27]
        # Boşlukları sil
        return qr_code.replace(' ', '')
