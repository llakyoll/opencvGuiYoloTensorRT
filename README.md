# OpenCV & CVUI Kişisel Notlar ve Hatırlatmalar

Bu README dosyası, OpenCV ve CVUI kullanımıyla ilgili önemli notları, ipuçlarını ve kendi projelerimde deneyimlediğim hatırlatmaları içerir. Hem kişisel referans hem de proje geliştirme rehberi olarak kullanılabilir.

---

## 1. OpenCV Genel Bilgiler

* **Kurulum:**

  ```bash
  pip install opencv-python
  pip install opencv-contrib-python
  pip install pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
  ```

* **Temel işlevler:**

  * `cv2.VideoCapture()` → Kamera veya video dosyasını açmak için
  * `cv2.imshow()` → Görüntüyü ekranda göstermek için
  * `cv2.imwrite()` → Görüntüyü dosya olarak kaydetmek için
  * `cv2.resize()` → Görüntüyü yeniden boyutlandırmak için
  * `cv2.waitKey(ms)` → Pencere güncelleme ve tuş yakalama

* **Kamera ayarları:**

  ```python
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
  cap.set(cv2.CAP_PROP_FPS, fps)
  ```

* **FPS hesaplama:**

  ```python
  import time
  start = time.time()
  # işlemler
  end = time.time()
  fps = 1 / (end - start)
  ```

* **BGR ve RGB:**
  OpenCV görüntüleri BGR formatında tutar, bazı kütüphaneler için RGB’ye çevrilmesi gerekir:

  ```python
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  ```

* **Video kaydı:**

  ```python
  out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
  out.write(frame)
  out.release()
  ```

---

## 2. CVUI Notları

* **Kurulum:**

  ```bash
  pip install cvui
  ```

* **Temel kullanım:**

  ```python
  import cvui
  cvui.init('Window Name')
  cvui.button(frame, x, y, w, h, "Button Text")
  cvui.update()
  ```

* **Kullanım prensibi:**

  1. Frame bir **NumPy array** olarak oluşturulur
  2. GUI öğeleri frame üzerine çizilir
  3. `cvui.update()` çağrısı ile güncelleme yapılır
  4. `cv2.imshow()` ile gösterim yapılır

* **Checkboxlar:**

  * `checkbox = [False]` şeklinde liste kullanılır
  * Tek seçenek aktif olacaksa diğer checkbox’lar False yapılır (mutually exclusive)

* **Window ve panel yönetimi:**

  * `cvui.window(frame, x, y, w, h, "Title")` → Panel/çerçeve ekler
  * Relative ölçümler, farklı ekran çözünürlükleri için önemli

* **Button yönetimi:**

  ```python
  if cvui.button(frame, x, y, w, h, "Click"):
      # işlem yapılır
  ```

* **Text ve çizgi ekleme:**

  * `cvui.text(frame, x, y, "Text", scale, color)`
  * `cv2.line(frame, pt1, pt2, color, thickness)`
Başlatma
import cvui
cvui.init('Pencere Adı')

Text (Yazı)
cvui.text(frame, x, y, "Yazı Metni", scale=0.5, color=0xFFFFFF)

Buton
if cvui.button(frame, x, y, width, height, "Button Text"):
    print("Button clicked!")

Checkbox
checked = [False]
if cvui.checkbox(frame, x, y, "Option 1", checked):
    print("Checkbox seçildi")

Slider
value = [50]
cvui.trackbar(frame, x, y, width, value, min_value, max_value)

Window (Panel)
cvui.window(frame, x, y, width, height, "Başlık")

Güncelleme ve Gösterim
cvui.update()
cv2.imshow("Pencere", frame)

Önemli Notlar

Frame temizliği: Döngü başında frame[:] = (R, G, B) ile arka plan temizlenmeli.

Koordinatlar ve boyutlar: Elemanların pencereden taşmamasına dikkat edin.

Checkbox ve Slider: Liste kullanımı zorunlu [False] veya [50].

Döngü bitirme: cv2.waitKey(20) ile ESC tuşu veya Exit butonu ile çıkılabilir.

* **Önemli ipucu:**
  CVUI GUI ile çalışırken **frame sürekli güncellenmeli**, yoksa buton ve checkboxlar çalışmaz

---

## 3. OpenCV + CVUI İpuçları

* Kamera ve GUI aynı döngüde çalıştırılırken FPS düşebilir

  * Çözüm: `resize` ile görüntüyü GUI alanına göre küçültmek
  * Ağır işlemler için frame kopyası alınarak işleme yapılabilir

* **OOP yapısı avantajları:**

  * Kamera (`Camera`) ve YOLO (`YOLOv8`) ayrı class’larda tutulmalı
  * GUI sadece kontrol ve görüntüleme işlevi görmeli

* **Kamera pause/resume:**

  * `cap.release()` ile durdur
  * `cap = cv2.VideoCapture(0)` ile başlat
  * CVUI butonları ile toggle yapılabilir

* **Snapshot alma:**

  * Butona basınca `cv2.imwrite("capture.jpg", img)` ile kaydedilebilir

* **Exit butonu:**

  * Sağ alt köşeye yerleştirmek kullanıcı deneyimi açısından iyi

---

## 4. Seri Bağlantı / Gelecek Plan Notları

* Modüler ve OOP yapısı önerilir:

  * **Camera class** → Tüm kamera yönetimi
  * **YOLO class** → Model yükleme ve tahmin
  * **GUI main** → Frame ve buton yönetimi
  * **Serial class** → Arduino / ESP32 bağlantısı

* Böylece:

  * Her modül bağımsız test edilebilir
  * GUI sadece arayüz yönetir
  * Yeni özellikler (filter, model değiştirme, seri haberleşme) kolayca eklenebilir

---

## 5. Önemli Hatırlatmalar

* OpenCV görüntüleri **BGR formatında**
* CVUI butonları ve checkboxlar **liste tipinde boolean** ile yönetilir
* GUI ve kamera aynı döngüde çalışırken **FPS düşebilir** → thread veya işlem ayrımı yapılabilir
* OOP yapısı hem **temiz kod** hem **modülerlik** sağlar
* Snapshot ve model tahmini gibi ağır işlemler için **orijinal frame korunmalı**
* Panel boyutlarını ve buton konumlarını **window boyutuna göre relative** hesaplamak iyi bir pratiktir

---

