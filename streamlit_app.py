import streamlit as st
import requests

# Konfigurasi halaman
st.set_page_config(page_title="TaniBot P2L Dashboard", page_icon="🌱", layout="wide")
st.title("🌱 Dashboard Pengujian AI - IoT Food Estate")
st.markdown("Dashboard ini terhubung langsung dengan backend FastAPI (localhost:8000).")

# URL API
API_BASE_URL = "http://localhost:8000/api"

# Sidebar untuk Input Sensor Global
st.sidebar.header("📊 Simulasi Data Sensor")
st.sidebar.markdown("Atur nilai sensor yang seolah-olah dikirim oleh alat IoT:")
temp_input = st.sidebar.slider("Suhu (°C)", min_value=15.0, max_value=40.0, value=28.0, step=0.1)
hum_input = st.sidebar.slider("Kelembapan (%)", min_value=30.0, max_value=90.0, value=65.0, step=0.1)
ph_input = st.sidebar.slider("pH Tanah", min_value=4.0, max_value=9.0, value=6.5, step=0.1)

sensor_data = {
    "temperature": temp_input,
    "humidity": hum_input,
    "ph": ph_input
}

# Menu Utama (Tabs)
tab1, tab2, tab3 = st.tabs(["🌱 Mode 1: Plant-First", "🔍 Mode 2: Soil-First", "💬 Mode 3: TaniBot Chat"])

# ---------------------------------------------------------
# TAB 1: PLANT-FIRST EVALUATOR
# ---------------------------------------------------------
with tab1:
    st.header("Mode Evaluasi Tanaman Spesifik")
    st.markdown("Validasi apakah tanah saat ini cocok untuk tanaman target Anda.")
    
    # Pilih tanaman dari dataset
    crop_list = ["cabai_rawit", "cabai_keriting", "tomat", "bayam", "kangkung", "selada", 
                 "terong", "timun", "bawang_merah", "bawang_putih", "sawi", "kacang_panjang", 
                 "seledri", "pare", "kemangi"]
    
    selected_crop = st.selectbox("Pilih Tanaman Target:", crop_list, index=2)
    
    if st.button("Evaluasi Tanah", key="btn_eval"):
        with st.spinner("Menganalisis..."):
            try:
                response = requests.post(f"{API_BASE_URL}/evaluate", json={
                    "crop_name": selected_crop,
                    "sensor_data": sensor_data
                })
                res_data = response.json()
                
                if res_data.get("success"):
                    data = res_data["data"]
                    st.subheader(f"{data['verdict_icon']} {data['verdict']}")
                    
                    # Tampilkan Insight dari Gemini
                    if res_data.get("insight"):
                        st.info(f"✨ **Insight AI:** {res_data['insight']}")
                        
                    # Detail per parameter
                    col1, col2, col3 = st.columns(3)
                    details = data["details"]
                    
                    with col1:
                        st.metric(label="Suhu", value=f"{temp_input} °C", delta=f"{details['temperature']['status']} {details['temperature']['icon']}", delta_color="off")
                    with col2:
                        st.metric(label="Kelembapan", value=f"{hum_input} %", delta=f"{details['humidity']['status']} {details['humidity']['icon']}", delta_color="off")
                    with col3:
                        st.metric(label="pH", value=f"{ph_input}", delta=f"{details['ph']['status']} {details['ph']['icon']}", delta_color="off")
                        
                    # Tampilkan Saran Perbaikan (Rule-based Remediation)
                    issues = []
                    if details['temperature']['status'] != 'IDEAL' and details['temperature'].get('remediation'):
                        issues.append(f"**Suhu:** {details['temperature']['remediation']['suggestion']} ({details['temperature']['remediation']['detail']})")
                    if details['humidity']['status'] != 'IDEAL' and details['humidity'].get('remediation'):
                        issues.append(f"**Kelembapan:** {details['humidity']['remediation']['suggestion']} ({details['humidity']['remediation']['detail']})")
                    if details['ph']['status'] != 'IDEAL' and details['ph'].get('remediation'):
                        issues.append(f"**pH:** {details['ph']['remediation']['suggestion']} ({details['ph']['remediation']['detail']})")
                        
                    if issues:
                        st.warning("🛠️ **Saran Perbaikan (Sistem Otomatis):**\n\n" + "\n\n".join(issues))
                        
                else:
                    st.error(res_data.get("error"))
            except Exception as e:
                st.error(f"Gagal terhubung ke API: {e}")

# ---------------------------------------------------------
# TAB 2: SOIL-FIRST RECOMMENDER
# ---------------------------------------------------------
with tab2:
    st.header("Mode Rekomendasi Cerdas")
    st.markdown("Temukan tanaman apa saja yang paling cocok dengan kondisi tanah saat ini.")
    
    top_n = st.number_input("Jumlah Rekomendasi (Top-N):", min_value=1, max_value=10, value=3)
    
    if st.button("Dapatkan Rekomendasi", key="btn_rec"):
        with st.spinner("Mencari kecocokan terbaik..."):
            try:
                response = requests.post(f"{API_BASE_URL}/recommend", json={
                    "sensor_data": sensor_data,
                    "top_n": top_n
                })
                res_data = response.json()
                
                if res_data.get("success"):
                    # Tampilkan Summary dari Gemini
                    if res_data.get("summary"):
                        st.success(f"✨ **Insight AI:** {res_data['summary']}")
                    
                    st.subheader("Rekomendasi Tanaman:")
                    for idx, rec in enumerate(res_data["recommendations"]):
                        prob_percent = rec['probability'] * 100
                        st.progress(rec['probability'], text=f"#{idx+1} - {rec['display_name']} ({prob_percent:.1f}%)")
                else:
                    st.error(res_data.get("error"))
            except Exception as e:
                st.error(f"Gagal terhubung ke API: {e}")

# ---------------------------------------------------------
# TAB 3: CHATBOT (TANIBOT)
# ---------------------------------------------------------
with tab3:
    st.header("Tanya Jawab TaniBot")
    st.markdown("Konsultasi masalah pertanian. TaniBot otomatis mengetahui data sensor Anda di sidebar.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Tampilkan chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Input chat
    if prompt := st.chat_input("Tanyakan sesuatu (misal: pupuk apa yang bagus untuk tomat?)..."):
        # Tambahkan ke UI
        st.chat_message("user").markdown(prompt)
        
        # Kirim ke API
        with st.spinner("TaniBot sedang mengetik..."):
            try:
                # Format history untuk API
                api_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                response = requests.post(f"{API_BASE_URL}/chat", json={
                    "message": prompt,
                    "sensor_context": sensor_data,
                    "history": api_history
                })
                res_data = response.json()
                
                if res_data.get("success"):
                    reply = res_data["reply"]
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                    
                    # Simpan ke state
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(res_data.get("error"))
            except Exception as e:
                st.error(f"Gagal terhubung ke API: {e}")
                
    if st.button("Hapus Obrolan", key="btn_clear_chat"):
        st.session_state.messages = []
        st.rerun()
