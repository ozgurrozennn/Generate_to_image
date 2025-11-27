import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import tempfile
import time
import requests
from io import BytesIO
from urllib.parse import quote

# Sayfa başlığı
st.title("🤖 Chatbot Resim Olusturma& Resimleri Pdf Cevirme")

# Sidebar
with st.sidebar:
    st.header(" Settings")

    st.markdown("### Nasıl Kullanılır:")
    st.markdown("1. **Resim Oluşturmak**: 'generate image [resim açıklaması]\nörnek:generate image a book'")
    st.markdown("2. **Convert to PDF**: Bilgisayardaki resimleri yükledikten sonra convert to pdf")

    if st.button(" Clear Chat"):
        st.session_state.messages = []
        st.session_state.uploaded_images = []
        st.session_state.generated_images = []
        st.rerun()

# Session state başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

# Chat geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "pdf":
            st.markdown(message["content"])
            st.download_button(
                label=" Download PDF",
                data=message["pdf_data"],
                file_name=message["filename"],
                mime="application/pdf",
                key=message["key"]
            )
        elif message.get("type") == "image":
            st.markdown(message["content"])
            if message.get("image_data"):
                st.image(message["image_data"], caption=message.get("caption", "Generated Image"))
        else:
            st.markdown(message["content"])

# File uploader
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


prompt = st.chat_input("Type your message or describe an image to generate...")


if prompt:
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    if ("convert to pdf" in prompt.lower() or
          "pdf yap" in prompt.lower() or
          "pdf oluştur" in prompt.lower()) and st.session_state.uploaded_images:

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

                        # Geçici dosya oluştur
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                        temp_path = tmp_file.name
                        tmp_file.close()

                        # Image'ı kaydet
                        image.save(temp_path, 'JPEG')
                        temp_files.append(temp_path)

                        # PDF'e sayfa ekle
                        pdf.add_page()
                        pdf.image(temp_path, x=10, y=10, w=190)

                    # PDF'i byte array'e kaydet
                    pdf_output = pdf.output(dest='S').encode('latin-1')

                    # Geçici dosyaları sil
                    for temp_path in temp_files:
                        try:
                            time.sleep(0.1)
                            os.remove(temp_path)
                        except:
                            pass

                    # Başarı mesajı ve download butonu
                    response = f"✅ Successfully converted {len(st.session_state.uploaded_images)} image(s) to PDF!"

                    # Mesajı kaydet
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


                    st.session_state.uploaded_images = []

                except Exception as e:
                    response = f"❌ Error converting images: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.error(response)

    # Resim oluşturma komutu kontrolü
    elif any(keyword in prompt.lower() for keyword in
             ["generate image", "create image", "draw", "resim oluştur", "resim yap", "çiz"]):

        with st.chat_message("assistant"):
            with st.spinner(" Generating image with AI..."):
                try:
                    # Temiz prompt oluştur
                    clean_prompt = prompt.lower()
                    for keyword in ["generate image", "create image", "draw", "resim oluştur", "resim yap", "çiz"]:
                        clean_prompt = clean_prompt.replace(keyword, "")
                    clean_prompt = clean_prompt.strip()

                    if not clean_prompt:
                        clean_prompt = "a beautiful landscape"

                    # Pollinations.ai API kullan
                    encoded_prompt = quote(clean_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

                    st.info(f"Generating: {clean_prompt}")

                    # Resmi indir
                    response_img = requests.get(image_url, timeout=60)
                    response_img.raise_for_status()

                    # PIL Image'a çevir
                    generated_image = Image.open(BytesIO(response_img.content))

                    # Session state'e kaydet
                    st.session_state.generated_images.append(generated_image)

                    response = f" Image generated successfully!\n\n**Prompt:** {clean_prompt}\n\n*Powered by Pollinations.ai*"

                    # Image bytes hazırla
                    image_bytes = BytesIO()
                    generated_image.save(image_bytes, format='PNG')
                    image_bytes.seek(0)

                    # Mesajı kaydet
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "type": "image",
                        "image_data": generated_image,
                        "caption": clean_prompt
                    })

                    st.markdown(response)
                    st.image(generated_image, caption=clean_prompt, use_container_width=True)

                    # Download butonu
                    st.download_button(
                        label="Download Image",
                        data=image_bytes.getvalue(),
                        file_name=f"generated_{int(time.time())}.png",
                        mime="image/png",
                        key=f"img_{len(st.session_state.messages)}"
                    )

                except Exception as e:
                    response = f"❌ Error generating image: {str(e)}\n\nPlease try again with a different prompt."
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.error(response)

    else:
        # Normal chat yanıtı
        with st.chat_message("assistant"):
            response = f"You said: **{prompt}**\n\n💡 **Try these:**\n- `generate image {prompt[8:]}` - Create AI images\n- Upload images → type `pdf` - Convert to PDF\n- Ask me anything!"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        with st.chat_message("assistant"):
            st.markdown(response)

    st.rerun()
