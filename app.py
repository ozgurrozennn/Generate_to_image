import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import tempfile
import time

# Sayfa başlığı
st.title("🤖 Chatbot with Image to PDF Converter")

# Session state başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []

# Chat geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "pdf":
            st.markdown(message["content"])
            st.download_button(
                label="📥 Download PDF",
                data=message["pdf_data"],
                file_name=message["filename"],
                mime="application/pdf",
                key=message["key"]
            )
        else:
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message or upload images...")

# File uploader (chat alanının üstünde, küçük)
uploaded_files = st.file_uploader(
    "📎 Attach images (then type 'convert to pdf' in chat)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Dosyalar yüklendiğinde session state'e kaydet
if uploaded_files:
    st.session_state.uploaded_images = uploaded_files
    st.info(f"📎 {len(uploaded_files)} image(s) attached. Type 'convert to pdf' to convert.")

# Chat mesajı geldiğinde
if prompt:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # PDF dönüştürme komutu kontrolü
    if ("convert to pdf" in prompt.lower() or 
        "pdf yap" in prompt.lower() or 
        "pdf oluştur" in prompt.lower() or
        "pdf" in prompt.lower()):
        
        if st.session_state.uploaded_images:
            with st.chat_message("assistant"):
                with st.spinner("Converting images to PDF..."):
                    try:
                        # PDF oluştur
                        pdf = FPDF()
                        temp_files = []
                        
                        for uploaded_file in st.session_state.uploaded_images:
                            # Image'ı aç
                            image = Image.open(uploaded_file)
                            
                            # RGB'ye çevir (PDF uyumluluğu için)
                            if image.mode in ('RGBA', 'P'):
                                image = image.convert('RGB')
                            
                            # Geçici dosya oluştur (delete=False ile)
                            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                            temp_path = tmp_file.name
                            tmp_file.close()  # Dosyayı kapat
                            
                            # Image'ı kaydet
                            image.save(temp_path, 'JPEG')
                            temp_files.append(temp_path)
                            
                            # PDF'e sayfa ekle
                            pdf.add_page()
                            
                            # Image boyutlarını hesapla ve ekle
                            pdf.image(temp_path, x=10, y=10, w=190)
                        
                        # PDF'i byte array'e kaydet - BURADA DEĞİŞİKLİK
                        pdf_output = pdf.output()  # .encode() kaldırıldı
                        
                        # Eğer string ise encode et, değilse direkt kullan
                        if isinstance(pdf_output, str):
                            pdf_output = pdf_output.encode('latin-1')
                        
                        # Geçici dosyaları sil
                        for temp_path in temp_files:
                            try:
                                time.sleep(0.1)  # Kısa bir bekleme
                                os.remove(temp_path)
                            except:
                                pass  # Silinmezse devam et
                        
                        # Başarı mesajı ve download butonu
                        response = f"✅ Successfully converted {len(st.session_state.uploaded_images)} image(s) to PDF!"
                        
                        # Mesajı kaydet (PDF data ile birlikte)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "type": "pdf",
                            "pdf_data": pdf_output,
                            "filename": "converted_images.pdf",
                            "key": f"pdf_{len(st.session_state.messages)}"
                        })
                        
                        st.markdown(response)
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_output,
                            file_name="converted_images.pdf",
                            mime="application/pdf",
                            key=f"pdf_{len(st.session_state.messages)}"
                        )
                        
                        # Yüklenen resimleri temizle
                        st.session_state.uploaded_images = []
                        
                    except Exception as e:
                        response = f"❌ Error converting images: {str(e)}"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        st.error(response)
        else:
            response = "❌ Please upload images first using the attachment button above."
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            with st.chat_message("assistant"):
                st.markdown(response)
    
    else:
        # Normal chat yanıtı
        response = f"You said: {prompt}\n\n💡 Tip: Upload images and type 'pdf' to convert them!"
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        with st.chat_message("assistant"):
            st.markdown(response)
    
    st.rerun()
