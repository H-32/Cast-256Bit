CAST-256 Implementation in Python
<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python Version">
<img src="https://img.shields.io/badge/Implementation-Modular-orange?style=for-the-badge" alt="Implementation">
<img src="https://img.shields.io/badge/Algorithm-CAST--256-green?style=for-the-badge" alt="Algorithm">
</p>

تطبيق برمجي متكامل لخوارزمية التشفير المتناظر CAST-256 بلغة بايثون، يتميز بهيكلية نظيفة وتقسيم برمجي يسهل الفهم والتطوير.

📝 نظرة عامة (Overview)
يعتبر CAST-256 من خوارزميات التشفير بنظام الكتل (Block Cipher) التي توفر حماية عالية ومرونة في الاستخدام.

حجم الكتلة (Block Size): 128 بت (16 بايت).

أحجام المفاتيح المدعومة: 128، 160، 192، 224، و256 بت.

نظام الحشو (Padding): PKCS#7.

Code/
├── helpers.py             # العمليات الحسابية والمنطقية الأساسية
├── round_functions.py     # دوال الجولات (f1, f2, f3)
├── sboxes.py              # جداول الاستبدال (S-boxes)
├── key_schedule.py        # توليد وتوسيع المفاتيح الفرعية
├── cipher.py              # تشفير وفك تشفير الكتل (128-bit)
└── text_cipher.py         # أدوات تشفير النصوص والحشو

⚙️ تفاصيل الموديلات (Modules Details)
1️⃣ العمليات المساعدة helpers.py
يحتوي هذا الموديل على العمليات منخفضة المستوى التي تعتمد عليها الخوارزمية:

add32 / sub32 / xor32: عمليات حسابية ومنطقية تضمن بقاء النتيجة ضمن نطاق 32 بت.

rol: تدوير البتات لليسار (Rotate Left).

Big-Endian Conversion: تحويل الكلمات (Words) إلى بايتات والعكس.

2️⃣ دوال الجولات round_functions.py
تنفيذ الدوال الثلاث الأساسية للـ CAST-256:

f1: تعتمد على الجمع و XOR والطرح.

f2: تعتمد على XOR والطرح والجمع.

f3: تعتمد على الطرح والجمع و XOR.
جميع الدوال تستخدم الـ S-boxes الأربعة بشكل متكامل.

3️⃣ جداول الاستبدال sboxes.py
تعريف الجداول الأربعة (S1, S2, S3, S4) حيث يحتوي كل جدول على 256 قيمة ست عشرية (Hexadecimal) مصممة لزيادة التعقيد والأمان.

4️⃣ جدولة المفاتيح key_schedule.py
المسؤول عن تحويل مفتاح التشفير الأساسي إلى مجموعة من المفاتيح الفرعية (Subkeys):

توليد جداول tm و tr.

استخراج مفاتيح الدوران (kr) ومفاتيح القناع (km).

دعم جولات التشفير الـ 12.

5️⃣ معالج التشفير cipher.py
المحرك الأساسي لتشفير كتلة واحدة (16 بايت):

تطبيق جولات الـ q (Forward Rounds) في النصف الأول.

تطبيق جولات الـ qbar (Reverse Rounds) في النصف الثاني.

6️⃣ تشفير النصوص text_cipher.py
واجهة المستخدم النهائية للتعامل مع النصوص:

PKCS#7 Padding: إضافة حشو للنصوص لتتناسب مع حجم الكتل.

Hex Utilities: تحويل النصوص المشفرة إلى صيغة Hex سهلة القراءة.

Normalizing Keys: توحيد طول مفتاح الدخول ليتناسب مع المعايير المطلوبة.

🚀 مثال على الاستخدام (Usage Example)
يمكنك البدء بتشفير نصوصك بسهولة باستخدام الكود التالي:
from Code.text_cipher import (
    encrypt_text_to_hex_with_size,
    decrypt_hex_to_text_with_size
)

# النص المراد تشفيره
plaintext = "Hello CAST-256 Implementation"
# مفتاح التشفير
key = "my-secret-key"

# عملية التشفير وتحويل النتيجة إلى Hex
cipher_hex = encrypt_text_to_hex_with_size(plaintext, key, key_size=32)
print(f"🔒 Ciphertext (HEX): {cipher_hex}")

# عملية فك التشفير
decrypted = decrypt_hex_to_text_with_size(cipher_hex, key, key_size=32)
print(f"🔓 Decrypted Text: {decrypted}")
