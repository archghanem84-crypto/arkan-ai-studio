import streamlit as st
import google.generativeai as genai
import requests
import base64

# --- إعدادات النظام ---
st.set_page_config(page_title="ARKA-OS Enterprise", layout="wide")
st.title("🏢 ARKA-OS | نظام التوليد المعماري المؤسسي")

# --- مفاتيح الربط ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"] # سنضع هذا في الـ Secrets
    genai.configure(api_key=GEMINI_API_KEY)
    gemini = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("يرجى التأكد من تعريف مفاتيح API في الـ Secrets.")

# --- واجهة المستخدم ---
engineer = st.text_input("اسم المهندس:", value="محمد غانم")
project_name = st.text_input("اسم المشروع:")
user_input = st.text_area("وصف الرؤية (مدينة، فيلا، موقع...):")

if st.button("🚀 بدء التنفيذ المؤسسي"):
    with st.status("جاري التحليل المعماري...", expanded=True) as status:
        # 1. الاستنتاج الذكي للسياق
        st.write("🧠 استنتاج سياق المشروع...")
        context_analysis = gemini.generate_content(f"""
        Analyze this: '{user_input}'.
        Classify it (e.g., City, Villa, Landscape).
        Then generate an English render prompt for NVIDIA SD 3.5, 
        and provide a short technical report (Concept, Materials, Lighting).
        Return in this format: [PROMPT] | [REPORT]
        """).text
        
        prompt_part, report_part = context_analysis.split('|')
        
        # 2. الربط مع NVIDIA (قوة الحوسبة)
        st.write("⚙️ جاري الريندر عبر NVIDIA...")
        invoke_url = "https://integrate.api.nvidia.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "stabilityai/stable-diffusion-3-5-large", "prompt": prompt_part.strip()}
        
        response = requests.post(invoke_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            img_data = response.json()['data'][0]['b64_json']
            status.update(label="اكتمل العمل!", state="complete")
            st.image(base64.b64decode(img_data), use_container_width=True)
            st.markdown("### 📋 التقرير الفني الذكي")
            st.info(report_part.strip())
        else:
            st.error(f"فشل الاتصال بـ NVIDIA: {response.text}")
