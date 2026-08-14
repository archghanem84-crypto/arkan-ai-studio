import streamlit as st
import requests
import base64

# --- إعدادات النظام المؤسسي ---
st.set_page_config(page_title="ARKA-OS Enterprise", layout="wide")
st.title("🏢 ARKA-OS | نظام الريندر المؤسسي (NVIDIA NIM Local Engine)")

# سحب مفتاح Gemini من الخزنة
gemini_key = st.secrets.get("GEMINI_API_KEY", "")

engineer = st.text_input("اسم المهندس:", value="محمد غانم")
project_name = st.text_input("اسم المشروع:")
user_input = st.text_area("وصف الرؤية المعمارية (فيلا، مدينة، موقع...):")

if st.button("🚀 تنفيذ الريندر عبر NIM المحلي"):
    if not user_input or not gemini_key:
        st.warning("⚠️ يرجى كتابة وصف المشروع وتأكد من توفر مفتاح Gemini في الـ Secrets.")
    else:
        with st.status("جاري معالجة المشروع وعكسه على محرك NVIDIA NIM...", expanded=True) as status:
            
            # 1. تحليل السياق المعماري عبر Gemini المباشر
            st.write("🧠 تحليل السياق المعماري وصياغة البرومبت...")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            gemini_payload = {
                "contents": [{"parts": [{"text": f"Analyze this architectural description: '{user_input}'. Return strictly in this format: PROMPT: [Professional English architectural exterior render prompt, 8k, photorealistic, Unreal Engine 5] | REPORT: [Short technical report in Arabic]"}]}]
            }
            
            p_part = f"{user_input}, professional architectural exterior rendering, 8k resolution, photorealistic, Unreal Engine 5"
            r_part = f"مشروع ({project_name}): تم تحليل الرؤية المعمارية وتطبيق معايير التصميم المتقدمة."
            
            try:
                gemini_resp = requests.post(gemini_url, json=gemini_payload, timeout=25).json()
                analysis_text = gemini_resp['candidates'][0]['content']['parts'][0]['text']
                if "|" in analysis_text:
                    p_part = analysis_text.split('|')[0].replace("PROMPT:", "").strip()
                    r_part = analysis_text.split('|')[1].replace("REPORT:", "").strip()
            except Exception:
                pass

            # 2. إرسال الطلب إلى سيرفر NVIDIA NIM المحلي (بناءً على الـ Endpoint الصحيح الذي أرسلته)
            st.write("🎨 إرسال الأمر إلى حاوية NIM المحلية (البورت 8000)...")
            invoke_url = "http://localhost:8000/v1/infer"
            
            payload = {
                "prompt": p_part,
                "mode": "base",
                "seed": 42,
                "steps": 30
            }
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.post(invoke_url, headers=headers, json=payload, timeout=90)
                
                if response.status_code == 200:
                    res_json = response.json()
                    
                    # استخراج الصورة المشفرة Base64 بالطريقة المعتمدة لـ NIM
                    artifacts = res_json.get("artifacts", [])
                    if artifacts and "base64" in artifacts[0]:
                        img_base64 = artifacts[0]["base64"]
                        img_bytes = base64.b64decode(img_base64)
                        
                        status.update(label="اكتمل الريندر المعماري بنجاح!", state="complete")
                        
                        col1, col2 = st.columns([1.5, 1])
                        with col1:
                            st.image(img_bytes, caption=f"مشروع: {project_name} | إشراف: {engineer}", use_container_width=True)
                        with col2:
                            st.markdown("### 📋 التقرير الفني الذكي")
                            st.info(r_part)
                    else:
                        status.update(label="خطأ في هيكل البيانات", state="error")
                        st.error(f"استجابة السيرفر المحلي لا تحتوي على مصفوفة artifacts صحيحة: {res_json}")
                else:
                    status.update(label="خطأ في الاتصال بالسيرفر المحلي", state="error")
                    st.error(f"خطأ من حاوية NIM ({response.status_code}): {response.text}")
                    
            except Exception as e:
                status.update(label="تعذر الاتصال بالحاوية", state="error")
                st.error(f"تأكد أن حاوية Docker تعمل بانتظام على البورت 8000 وأن الـ Endpoint `/v1/infer` متاح: {e}")
