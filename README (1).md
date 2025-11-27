# 🤖 AI Chatbot with Image Generator & PDF Converter

Gemini API ile resim oluşturma ve yüklenen görselleri PDF'e dönüştürme özelliklerine sahip Streamlit uygulaması.

## 🌟 Özellikler

- **Resim Oluşturma**: Gemini API kullanarak metin açıklamasından resim oluşturma
- **PDF Dönüştürme**: Yüklenen görselleri tek bir PDF dosyasına dönüştürme
- **Chat Arayüzü**: Gemini ile sohbet etme
- **Kolay Kullanım**: Basit ve sezgisel arayüz

## 📋 Gereksinimler

- Python 3.8+
- Gemini API Key ([buradan alabilirsiniz](https://makersuite.google.com/app/apikey))

## 🚀 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
streamlit run app.py
```

3. Tarayıcınızda açılan sayfada:
   - Sidebar'dan Gemini API Key'inizi girin
   - Kullanmaya başlayın!

## 💡 Kullanım

### Resim Oluşturma
Chat kutusuna şunları yazabilirsiniz:
- `generate image a cat on the moon`
- `create image beautiful sunset`
- `resim oluştur deniz kenarında köpek`
- `çiz futuristik şehir`

### PDF Dönüştürme
1. "📎 Attach images" butonuyla resimlerinizi yükleyin
2. Chat kutusuna `convert to pdf` veya `pdf` yazın
3. PDF'i indirin!

### Chat
Normal mesajlar yazarak Gemini ile sohbet edebilirsiniz.

## ⚠️ Notlar

- Imagen özelliği için API key'inizin Imagen erişimi olması gerekir
- Ücretsiz Gemini API sınırlamaları geçerlidir
- Büyük resimlerin PDF'e dönüşümü biraz zaman alabilir

## 🔑 API Key Alma

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan key'i kopyalayın

## 📝 Lisans

MIT License
