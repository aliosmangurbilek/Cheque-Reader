from pylibdmtx import pylibdmtx
from PIL import Image

class QRReader:
    def read_qr_code(self, image_path):
        image = Image.open(image_path)
        decoded_objects = pylibdmtx.decode(image)
        if decoded_objects:
            print(decoded_objects)
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
