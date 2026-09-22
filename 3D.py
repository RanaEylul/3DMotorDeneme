import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Araba Motoru Kalite Kontrol Testi", page_icon="🔧", layout="centered"
)

st.title("🔧 Fabrika Kalite Kontrol: Motor 360° İnceleme Testi")
st.markdown(
    "Aşağıdaki kaydırıcıyı (slider) kullanarak motoru **360 derece** döndürün"
    " ve hatalı parçayı tespit edin."
)

# Örnek motor görselleri listesi (Gerçek projede kendi motor görsellerinizin yollarını ekleyebilirsiniz)
# Şimdilik yer tutucu (placeholder) görseller kullanıyoruz:
images = [
    "https://picsum.photos/seed/motor1/600/400",  # Açı 1 (Ön)
    "https://picsum.photos/seed/motor2/600/400",  # Açı 2 (Yan)
    "https://picsum.photos/seed/motor3/600/400",  # Açı 3 (Arka)
    "https://picsum.photos/seed/motor4/600/400",  # Açı 4 (Hatalı Bölge)
]

# Slider ile açı seçimi (0 ile 3 aralığında)
angle_index = st.slider(
    "Motor Dönüş Açısı",
    min_value=0,
    max_value=len(images) - 1,
    value=0,
    format="Açı Adımı: %d",
)

# Seçilen açıya ait görseli ekrana basma
st.image(
    images[angle_index],
    caption=f"Motor Görünümü - Adım {angle_index + 1}",
    use_container_width=True,
)

# --- TEST SORUSU ---
st.markdown("---")
st.subheader("📝 Kalite Kontrol Sınavı")
st.write(
    "İncelediğiniz motor fotoğraflarına dayanarak soruyu yanıtlayın:"
)

user_answer = st.radio(
    "Soru: Hangi görselde/açıda motorda anormal bir durum (hata) tespit"
    " ettiniz?",
    (
        "Seçiniz...",
        "Adım 1 (Ön taraf temiz)",
        "Adım 2 (Yan bağlantılar sağlam)",
        "Adım 3 (Arka blok normal)",
        "Adım 4 (Parçada çatlak/hata var)",
    ),
)

if st.button("Sonucu Gönder"):
  if user_answer == "Adım 4 (Parçada çatlak/hata var)":
    st.success(
        "🎉 TEBRİKLER! Hatayı doğru açıda (4. adımda) başarıyla tespit"
        " ettiniz."
    )
    st.balloons()
  elif user_answer == "Seçiniz...":
    st.warning("Lütfen bir seçenek işaretleyin.")
  else:
    st.error(
        "❌ Yanlış cevap! Seçtiğiniz bölgede bir hata bulunmuyor. Tekrar"
        " inceleyin."
    )