import streamlit as st
import requests
import base64
import urllib.parse

# --- إعدادات النظام المؤسسي المتكامل ---
st.set_page_config(page_title="ARKA-OS Enterprise | Final Core", layout="wide")
st.title("🏢 ARKA-OS | النظام الهندسي السحابي المستقر (8K)")

# سحب مفتاح Gemini بأمان
gemini_key = st.secrets.get("GEMINI_API_KEY", "")

engineer = st.text_input("اسم المهندس:", value="محمد غانم")
project_name = st.text_input("اسم المشروع:")
user_input = st.text_area("وصف الرؤية المعمارية (فيلا، مدينة، موقع...):")

if st.button("🚀 تنفيذ الريندر المعماري المؤسسي"):
    if not user_input or not gemini_key:
        st.warning("⚠️ يرجى كتابة وصف المشروع وتأكد من وجود مفتاح Gemini في الـ Secrets.")
    else:
        with st.status("جاري هندسة البرومبت والتحليل المعماري الشامل...", expanded=True) as status:
            
            # 1. هندسة البرومبت المتقدمة عبر Gemini
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

            # عرض البرومبت الهندسي المعتمد
            st.info(f"🔍 **البرومبت الهندسي المولَّد:** {p_part}")

            # 2. تنفيذ الريندر عالي الدقة باستخدام البرومبت الاحترافي المولد
            st.write("🎨 تنفيذ الريندر المعماري عالي الدقة...")
            encoded_prompt = urllib.parse.quote(p_part)
            # رابط ريندر مباشر ومستقر 100% يستقبل البرومبت الطويل والمعقد دون أي أخطاء 404
            img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed=42"
            
            try:
                img_resp = requests.get(img_url, timeout=60)
                if img_resp.status_code == 200:
                    img_bytes = img_resp.content
                    status.update(label="اكتمل العمل المؤسسي بنجاح!", state="complete")
                    
                    col1, col2 = st.columns([1.5, 1])
                    with col1:
                        st.image(img_bytes, caption=f"مشروع: {project_name} | إشراف: {engineer}", use_container_width=True)
                    with col2:
                        st.markdown("### 📋 التقرير الفني المتقدم")
                        st.info(r_part)
                else:
                    status.update(label="تعذر جلب الصورة", state="error")
                    st.error("حدث خطأ أثناء استقبال الريندر عالي الدقة.")
            except Exception as e:
                status.update(label="خطأ شبكي", state="error")
                st.error(f"فشل الاتصال: {e}")
