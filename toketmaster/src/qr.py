import cv2
import qrcode


def create_QR(tasa_id: str):
    img = qrcode.make(tasa_id)
    img.save('qr.png')

    return img


def read_QR(path_to_qr: str) -> str:
    qr = cv2.imread('qr.png')
    detector = cv2.QRCodeDetector()
    tasa_index, _, _ = detector.detectAndDecode(qr)
    
    return tasa_index
