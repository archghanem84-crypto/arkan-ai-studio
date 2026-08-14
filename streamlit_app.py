import streamlit as st
import requests
import base64

# --- إعدادات النظام ---
st.set_page_config(page_title="ARKA-OS Enterprise", layout="wide")
st.title("🏢 ARKA-OS | النظام المؤسسي المستقر")

# سحب المفاتيح بأمان
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
nvidia_key = st.secrets.get("NVIDIA_API_KEY", "")

engineer = st.text_input("اسم المهندس:", value="محمد غانم")
project_name = st.text_input("اسم المشروع:")
user_input = st.text_area("وصف الرؤية (مدينة، فيلا، موقع...):")

if st.button("🚀 تنفيذ المؤسسة"):
    if not user_input or not gemini_key or not nvidia_key:
        st.error("⚠️ تأكد من كتابة الوصف ووجود مفاتيح API في الـ Secrets.")
    else:
        with st.status("جاري معالجة المشروع...", expanded=True) as status:
            
            # 1. الاتصال الآمن المباشر بـ Gemini (بدون مكتبة، عبر HTTP)
            st.write("🧠 تحليل السياق عبر اتصال مباشر...")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            gemini_payload = {
                "contents": [{"parts": [{"text": f"Analyze: '{user_input}'. Return only: PROMPT: [English render prompt] | REPORT: [Arabic architectural report]"}]}]
            }
            
            analysis_text = ""
            try:
                gemini_resp = requests.post(gemini_url, json=gemini_payload, timeout=30).json()
                analysis_text = gemini_resp['candidates'][0]['content']['parts'][0]['text']
            except:
                analysis_text = "PROMPT: Architectural exterior view, photorealistic, 8k | REPORT: تصميم معماري احترافي."

            p_part = analysis_text.split('|')[0].replace("PROMPT:", "").strip()
            r_part = analysis_text.split('|')[1].replace("REPORT:", "").strip()

            # 2. الاتصال المباشر بـ NVIDIA
            st.write("🎨 ريندر عبر NVIDIA...")
            nvidia_url = "https://integrate.api.nvidia.com/v1/images/generations"
            nvidia_headers = {"Authorization": f"Bearer {nvidia_key}", "Content-Type": "application/json"}
            nvidia_payload = {"model": "stabilityai/stable-diffusion-3-5-large", "prompt": p_part}
            
            resp = requests.post(nvidia_url, headers=nvidia_headers, json=nvidia_payload, timeout=45)
            
            if resp.status_code == 200:
                img_data = resp.json()['data'][0]['b64_json']
                status.update(label="اكتمل العمل!", state="complete")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(base64.b64decode(img_data), caption=f"مشروع: {project_name}", use_container_width=True)
                with col2:
                    st.markdown("### 📋 التقرير الفني الذكي")
                    st.info(r_part)
            else:
                st.error(f"خطأ NVIDIA: {resp.text}")
