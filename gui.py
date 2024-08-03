from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from PIL import Image as PILImage
import numpy as np
import threading
from qr_reader import QRReader
from micr_reader import MICRReader


class StyledButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.2, 0.6, 0.8, 1)
        self.text_color = (1, 1, 1, 1)
        self.font_size = 18
        self.bold = True
        self.size_hint = (None, None)
        self.size = (200, 50)
        self.bind(on_press=self.on_press_effect)
        self.bind(on_release=self.on_release_effect)

    def on_press_effect(self, instance):
        self.md_bg_color = (0.1, 0.5, 0.7, 1)

    def on_release_effect(self, instance):
        self.md_bg_color = (0.2, 0.6, 0.8, 1)

class CheckScannerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Koyu tema
        self.theme_cls.primary_palette = "BlueGray"

        self.title = 'Check Scanner'
        Window.size = (900, 700)
        Window.bind(on_dropfile=self._on_file_drop)

        self.layout = MDFloatLayout()

        self.img = KivyImage(size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True, pos_hint={'x': 0, 'top': 1.1})
        self.layout.add_widget(self.img)

        self.scroll_view = ScrollView(size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0})
        self.result_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))

        self.micr_label = MDLabel(text='MICR Kodu:', size_hint_y=None, height=20)
        self.result_layout.add_widget(self.micr_label)

        self.micr_code_input = MDTextField(readonly=True, multiline=True, size_hint_y=None, height=50)
        self.result_layout.add_widget(self.micr_code_input)

        self.qr_label = MDLabel(text='QR Kodu:', size_hint_y=None, height=20)
        self.result_layout.add_widget(self.qr_label)

        self.qr_code_input = MDTextField(readonly=True, multiline=True, size_hint_y=None, height=50)
        self.result_layout.add_widget(self.qr_code_input)

        self.scroll_view.add_widget(self.result_layout)
        self.layout.add_widget(self.scroll_view)

        self.load_button = StyledButton(text='Görüntü Yükle', pos_hint={'x': 0.1, 'y': 0.30})
        self.load_button.bind(on_press=self.show_file_chooser)
        self.layout.add_widget(self.load_button)

        self.qr_button = StyledButton(text='QR Oku', pos_hint={'x': 0.35, 'y': 0.30})
        self.qr_button.bind(on_press=self.read_qr)
        self.layout.add_widget(self.qr_button)

        self.micr_button = StyledButton(text='MICR Oku', pos_hint={'x': 0.55, 'y': 0.30})
        self.micr_button.bind(on_press=self.read_micr)
        self.layout.add_widget(self.micr_button)

        self.compare_button = StyledButton(text='Karşılaştır', pos_hint={'x': 0.75, 'y': 0.30})
        self.compare_button.bind(on_press=self.compare_codes)
        self.layout.add_widget(self.compare_button)

        self.qr_code = None
        self.micr_code = None
        self.qr_reader = QRReader()
        self.micr_reader = MICRReader(tessdata_dir=r'C:\Program Files\Tesseract-OCR\tessdata')

        # Initial image to display
        initial_image_path = "resources/ornek_cek.png"
        self.load_initial_image(initial_image_path)

        # FileManager for file selection
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )

        return self.layout

    def load_initial_image(self, file_path):
        self.update_image_source(file_path)
        self.qr_code = None
        self.micr_code = None

    def show_file_chooser(self, *args):
        self.file_manager.show('/')

    def select_path(self, path):
        self.load_image([path])
        self.file_manager.close()

    def exit_manager(self, *args):
        self.file_manager.close()

    def load_image(self, selection, popup=None):
        file_path = selection[0] if selection else None
        if file_path:
            self.update_image_source(file_path)
            self.qr_code = None
            self.micr_code = None
            if popup:
                popup.dismiss()

    def update_image_source(self, file_path):
        pil_image = PILImage.open(file_path)
        self.update_image_texture(pil_image)
        self.img.source = file_path
        self.img.reload()

    def update_image_texture(self, pil_image):
        data = np.array(pil_image)
        buf = data.tobytes()
        texture = Texture.create(size=(data.shape[1], data.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.img.texture = texture

    def read_qr(self, instance):
        self.show_loading_popup()
        threading.Thread(target=self._read_qr_thread).start()

    def _read_qr_thread(self):
        file_path = self.img.source if self.img.source else None
        if file_path:
            self.qr_code = self.qr_reader.read_qr_code(file_path)
            Clock.schedule_once(lambda dt: self.update_qr_code_input(), 0)

    def update_qr_code_input(self):
        self._hide_loading_popup()
        if self.qr_code:
            self.qr_code_input.text = f'{self.qr_code}'
        else:
            self.qr_code_input.text = 'QR kodu okunamadı.'

    def read_micr(self, instance):
        self.show_loading_popup()
        threading.Thread(target=self._read_micr_thread).start()

    def _read_micr_thread(self):
        file_path = self.img.source if self.img.source else None
        if file_path:
            try:
                self.micr_code, micr_image = self.micr_reader.read_micr_code(file_path)
                Clock.schedule_once(lambda dt: self.update_label_with_micr_code(), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_label_with_error(), 0)

    def update_label_with_micr_code(self):
        self._hide_loading_popup()
        if self.micr_code:
            self.micr_code_input.text = f'{self.micr_code}'
        else:
            self.micr_code_input.text = 'MICR kodu okunamadı.'

    def update_label_with_error(self):
        self._hide_loading_popup()
        self.micr_code_input.text = 'MICR kodu okunamadı.'

    def compare_codes(self, instance):
        if self.qr_code and self.micr_code:
            cleaned_qr_code = self.clean_code(self.qr_code)
            cleaned_micr_code = self.clean_code(self.micr_code)
            result_text = f'İşlenmiş QR Kodu: {cleaned_qr_code}\nİşlenmiş MICR Kodu: {cleaned_micr_code}\n'
            if cleaned_qr_code == cleaned_micr_code:
                result_text += 'Sonuçlar: QR kodu ve MICR kodu aynı.'
            else:
                result_text += 'Sonuçlar: QR kodu ve MICR kodu farklı.'
            Clock.schedule_once(lambda dt: self.show_result_popup(result_text), 0)
        else:
            result_text = 'Sonuçlar: Önce QR ve MICR kodlarını okuyun.'
            Clock.schedule_once(lambda dt: self.show_result_popup(result_text), 0)

    def clean_code(self, code):
        return ''.join(filter(str.isdigit, code))

    def show_result_popup(self, text):
        self.dialog = MDDialog(title='Sonuç', text=text, size_hint=(0.6, 0.4), buttons=[
            MDRaisedButton(text='Tamam', on_release=lambda x: self.dialog.dismiss())
        ])
        self.dialog.open()

    def _on_file_drop(self, window, file_path):
        file_path = file_path.decode('utf-8')
        self.update_image_source(file_path)
        self.qr_code = None
        self.micr_code = None

    def show_loading_popup(self):
        self.progress_bar = ProgressBar(max=1)
        self.loading_popup = MDDialog(title='İşlem Yapılıyor', type="custom", content_cls=self.progress_bar, size_hint=(0.6, 0.2))
        self.loading_popup.open()
        Clock.schedule_interval(self._update_progress, 0.1)

    def _update_progress(self, dt):
        if self.progress_bar.value >= self.progress_bar.max:
            self.progress_bar.value = 0
        self.progress_bar.value += 0.1

    def _hide_loading_popup(self):
        Clock.schedule_once(lambda dt: self.loading_popup.dismiss(), 0)

if __name__ == '__main__':
    CheckScannerApp().run()
