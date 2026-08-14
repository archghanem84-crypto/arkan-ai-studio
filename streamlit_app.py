import streamlit as st
import requests
import base64

st.set_page_config(page_title="ARKA-OS Enterprise", layout="wide")
st.title("🏢 ARKA-OS | النظام الهندسي المعتمد (NVIDIA Cloud)")

gemini_key = st.secrets.get("GEMINI_API_KEY", "")
nvidia_key = st.secrets.get("NVIDIA_API_KEY", "")

user_input = st.text_area("وصف الرؤية المعمارية:")

if st.button("🚀 تنفيذ"):
    with st.status("معالجة هندسية...", expanded=True) as status:
        
        # 1. صياغة البرومبت (Gemini)
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        # إجبار النموذج على إخراج كود إنجليزي تقني صارم
        gemini_payload = {"contents": [{"parts": [{"text": f"Generate a strict architectural exterior prompt for '{user_input}'. NO humans, NO faces. Only building, facade, materials, 8k. PROMPT: [text]"}]}]}
        
        p_part = requests.post(gemini_url, json=gemini_payload).json()['candidates'][0]['content']['parts'][0]['text']
        
        # 2. الريندر (NVIDIA API المباشر)
        # هذا الرابط هو المسار الرسمي لـ Stability AI على NVIDIA Cloud
        nvidia_url = "https://integrate.api.nvidia.com/v1/images/generations"
        
        payload = {
            "model": "stabilityai/stable-diffusion-3-5-large",
            "prompt": p_part,
            "negative_prompt": "people, human, face, portrait, naked, skin, body, person", # هذا هو الحل الجذري لمنع النتائج غير المعمارية
            "width": 1024,
            "height": 576
        }
        
        headers = {"Authorization": f"Bearer {nvidia_key}", "Content-Type": "application/json"}
        
        resp = requests.post(nvidia_url, headers=headers, json=payload)
        
        if resp.status_code == 200:
            img_data = resp.json()['data'][0]['b64_json']
            st.image(base64.b64decode(img_data), use_container_width=True)
        else:
            st.error(f"خطأ NVIDIA: {resp.status_code} - {resp.text}")
