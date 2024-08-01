# Check Scanner App

Bu proje, çek üzerindeki QR kodlarını ve MICR kodlarını okuyan ve karşılaştıran bir uygulamadır. Uygulama, Kivy kullanılarak oluşturulmuş bir grafik arayüzüne sahiptir ve Tesseract OCR ile MICR kodlarını tanımak için kullanılır.

## Gereksinimler

- Python 3.12
- Tesseract OCR
- Kütüphaneler:
  - kivy==2.1.0
  - Pillow==9.2.0
  - numpy==1.23.3
  - pylibdmtx==0.1.9
  - pytesseract==0.3.9
  - opencv-python==4.6.0.66

## Kurulum

### Python ve Gerekli Kütüphaneler

1. **Python 3.12'yi Kurun:**

    [Python'un resmi web sitesinden](https://www.python.org/downloads/) Python 3.12'yi indirin ve yükleyin.

2. **Virtual Environment (Sanal Ortam) Oluşturma:**

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # Linux ve macOS için
    myenv\Scripts\activate     # Windows için
    ```

3. **Gerekli Kütüphaneleri Yükleyin:**

    ```bash
    pip install kivy==2.1.0 Pillow==9.2.0 numpy==1.23.3 pylibdmtx==0.1.9 pytesseract==0.3.9 opencv-python==4.6.0.66
    ```
    
    **yada terminalden şu komutu girin:**
   
    ```bash
    pip install -r requirements.txt
    ```

### Tesseract OCR Kurulumu

1. **Tesseract OCR'ı İndirin ve Kurun:**

    Tesseract'ın [resmi GitHub sayfasından](https://github.com/tesseract-ocr/tesseract) veya [Tesseract'ın resmi web sitesinden](https://tesseract-ocr.github.io/tessdoc/Downloads.html) indirin ve yükleyin.

2. **Tesseract Yolunu Ayarlayın:**

    Tesseract'ı yükledikten sonra, kurulum yolunu sisteminizin PATH değişkenine eklemeniz gerekecektir. Örneğin, Windows için kurulum yolu genellikle `C:\Program Files\Tesseract-OCR\tesseract.exe` olacaktır.

3. **Tesseract Data Dosyalarını İndirin:**

    Tesseract için gerekli veri dosyalarını (tessdata) indirmeniz gerekmektedir. Bunları [Tesseract tessdata sayfasından](https://github.com/tesseract-ocr/tessdata) indirebilirsiniz. Özellikle `e13b.traineddata` dosyasına ihtiyacınız olacak. Bu dosyayı indirip Tesseract'ın tessdata dizinine yerleştirin.

    ```plaintext
    C:\Program Files\Tesseract-OCR\tessdata
    ```
4. Dizinde bulunan e13b.tessdata dosyasını C:\Program Files\Tesseract-OCR\tessdata dizinine kopyalamayı unutmayın!!!

## Proje Yapısı

```plaintext
check-scanner-app/
│
├── main.py               # Ana uygulama dosyası
├── qr_reader.py          # QR kod okuyucu modülü
├── micr_reader.py        # MICR kod okuyucu modülü
├── README.md             # Bu dosya
├── requirements.txt      # Gerekli Python kütüphanelerinin listesi
└── images/
    └── ornek_cek.png     # Örnek çek görseli
