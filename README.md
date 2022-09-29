# Barcode-Reader
Barcode and QRcode Reader for rotated image.

---

### Description

if GUImode,

Required items : Sentech_GigE_CAM, Arduino, Sensor(photo sensor), Light

Sensor and Light are controlled by Arduino.

The PC communicates with serial through Arduino.

---

## Install

```
git clone https://github.com/tdat97/Barcode-Reader.git
cd Barcode-Reader
pip install -r requirments.txt
```

---

#### Console mode

example
```
python run.py --image ./temp/mybar.jpg
```
you can check result in "./image"

Annotation Image
![mybar](https://user-images.githubusercontent.com/48349693/192415204-297df3a3-6eec-4fcc-ac6f-155b03da7001.jpg)

Debug Image
![mybar](https://user-images.githubusercontent.com/48349693/192415276-c309650a-2fb0-4dc4-8691-352faee03bd2.jpg)

---

#### GUI mode

example
```
python run.py
```

GUI Capture

![캡처](https://user-images.githubusercontent.com/48349693/192426808-006d0ad8-9e16-45ad-ac76-46fb8857eee1.PNG)

