def get_summarization_prompt(top_crops: list, sensor_data: dict) -> str:
    """
    Generates the prompt for Mode 2 (Soil-First).
    """
    crop_names = [crop["display_name"] for crop in top_crops]
    crops_str = ", ".join(crop_names)
    
    prompt = f"""
Kamu adalah asisten pertanian pintar (TaniBot) untuk aplikasi P2L (Pekarangan Pangan Lestari) di perkotaan.
Pengguna mengecek tanahnya tanpa target tanaman spesifik. 
Sistem AI telah merekomendasikan tanaman berikut yang paling cocok ditanam di pot/pekarangan mereka: {crops_str}.

Data sensor tanah:
- Suhu: {sensor_data['temperature']}°C
- Kelembapan: {sensor_data['humidity']}%
- pH: {sensor_data['ph']}

Tugasmu:
Buatkan paragraf singkat (maksimal 2-3 kalimat) menggunakan bahasa Indonesia yang santai dan memotivasi.
Beri tahu pengguna bahwa kondisi tanah mereka bagus untuk tanaman-tanaman tersebut dan dorong mereka untuk mulai menanam hari ini.
Jangan menggunakan format poin-poin.
"""
    return prompt.strip()
