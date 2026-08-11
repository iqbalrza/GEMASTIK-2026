def get_insight_prompt(crop_name: str, verdict: str, sensor_data: dict, evaluation_details: dict) -> str:
    """
    Generates the prompt for Mode 1 (Plant-First).
    """
    temp_status = evaluation_details["temperature"]["status"]
    hum_status = evaluation_details["humidity"]["status"]
    ph_status = evaluation_details["ph"]["status"]
    
    prompt = f"""
Kamu adalah asisten pertanian pintar (TaniBot) untuk aplikasi P2L (Pekarangan Pangan Lestari) di perkotaan.
Pengguna mengecek kecocokan tanahnya untuk menanam **{crop_name}**.

Data sensor tanah saat ini:
- Suhu: {sensor_data['temperature']}°C (Status: {temp_status})
- Kelembapan: {sensor_data['humidity']}% (Status: {hum_status})
- pH: {sensor_data['ph']} (Status: {ph_status})

Keputusan keseluruhan: **{verdict}**

Tugasmu:
Buatkan paragraf singkat (maksimal 3 kalimat) menggunakan bahasa Indonesia yang ramah, santai, dan mudah dimengerti oleh warga awam/ibu-ibu PKK.
Berikan satu saran praktis paling penting jika ada parameter yang tidak ideal. Jika semua ideal, berikan semangat untuk mulai menanam.
Jangan menggunakan format poin-poin (bullet points).
"""
    return prompt.strip()
