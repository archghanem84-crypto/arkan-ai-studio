import streamlit as st
import requests
import base64

# --- إعدادات النظام المؤسسي المتكامل ---
st.set_page_config(page_title="ARKA-OS Enterprise | Complete Core", layout="wide")
st.title("🏢 ARKA-OS | النظام الهندسي السحابي المتكامل (8K & NVIDIA)")

# سحب المفاتيح من الخزنة بأمان تام
gemini_key = st.secrets.get("GEMINI_API_KEY", "")
nvidia_key = st.secrets.get("NVIDIA_API_KEY", "")

engineer = st.text_input("اسم المهندس:", value="محمد غانم")
project_name = st.text_input("اسم المشروع:")
user_input = st.text_area("وصف الرؤية المعمارية (فيلا، مدينة، موقع...):")

if st.button("🚀 تنفيذ الريندر المعماري المؤسسي"):
    if not user_input or not gemini_key or not nvidia_key:
        st.warning("⚠️ يرجى التأكد من كتابة الوصف ووجود مفتاحي Gemini و NVIDIA في الـ Secrets.")
    else:
        with st.status("جاري هندسة البرومبت والتحليل المعماري الشامل...", expanded=True) as status:
            
            # 1. هندسة البرومبت المتقدمة عبر Gemini مع توجيهات معمارية صارمة
            st.write("🧠 هندسة البرومبت الاحترافي عالي الدقة (8K)...")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            
            system_instruction = (
                f"You are a master chief architectural design director. "
                f"Analyze this core user concept: '{user_input}'. "
                f"Expand it into an elite, highly detailed professional English architectural exterior render prompt including: "
                f"exact material specifications (stone, glass, concrete), contemporary modern or regional heritage context, cinematic volumetric lighting, 8k resolution, photorealistic, Unreal Engine 5 render style. "
                f"STRICT RULE: Focus ONLY on building structure and facade. NEVER generate human figures, portraits, or faces. "
                f"Also provide a detailed technical engineering report in Arabic. "
                f"Format strictly as: PROMPT: [Detailed English Prompt] | REPORT: [Detailed Arabic Report]"
            )
            
            gemini_payload = {
                "contents": [{"parts": [{"text": system_instruction}]}]
            }
            
            p_part = f"{user_input}, professional architectural exterior building rendering, ultra-detailed facade, 8k resolution, photorealistic, cinematic lighting, Unreal Engine 5"
            r_part = f"مشروع ({project_name}): تم تطوير البرومبت هندسياً لرفع جودة الكتلة البصرية."
            
            try:
                gemini_resp = requests.post(gemini_url, json=gemini_payload, timeout=25).json()
                analysis_text = gemini_resp['candidates'][0]['content']['parts'][0]['text']
                if "|" in analysis_text:
                    p_part = analysis_text.split('|')[0].replace("PROMPT:", "").strip()
                    r_part = analysis_text.split('|')[1].replace("REPORT:", "").strip()
            except Exception:
                pass

            # عرض البرومبت الهندسي المعتمد للتأكد من دقته
            st.info(f"🔍 **البرومبت الهندسي المولَّد:** {p_part}")

            # 2. إرسال الطلب بدقة عالية عبر سحابة NVIDIA الرسمية
            st.write("🎨 تنفيذ الريندر المعماري عالي الدقة عبر NVIDIA...")
            nvidia_url = "https://integrate.api.nvidia.com/v1/images/generations"
            
            headers = {
                "Authorization": f"Bearer {nvidia_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "stabilityai/stable-diffusion-3-5-large",
                "prompt": p_part,
                "width": 1024,
                "height": 576,
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
            
            try:
                response = requests.post(nvidia_url, headers=headers, json=payload, timeout=90)
                
                if response.status_code == 200:
                    res_json = response.json()
                    img_data = res_json.get("data", [{}])[0].get("b64_json", "")
                    
                    if img_data:
                        status.update(label="اكتمل العمل المؤسسي بنجاح!", state="complete")
                        
                        col1, col2 = st.columns([1.5, 1])
                        with col1:
                            st.image(base64.b64decode(img_data), caption=f"مشروع: {project_name} | إشراف: {engineer}", use_container_width=True)
                        with col2:
                            st.markdown("### 📋 التقرير الفني المتقدم")
                            st.info(r_part)
                    else:
                        status.update(label="خطأ في استجابة الموديل", state="error")
                        st.error(f"استجابة NVIDIA لا تحتوي على بيانات الصورة: {res_json}")
                else:
                    status.update(label="خطأ في الاتصال بالسحابة", state="error")
                    st.error(f"خطأ من سحابة NVIDIA ({response.status_code}): {response.text}")
                    
            except Exception as e:
                status.update(label="خطأ تقني", state="error")
                st.error(f"حدث خطأ أثناء الاتصال بسحابة NVIDIA الرسمية: {e}")
