import streamlit as st
import google.generativeai as genai
import urllib.parse

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان المعمارية (النسخة الاحترافية)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>نظام التحليل الهندسي المتقدم والتوليد البصري</p>", unsafe_allow_html=True)
st.divider()

# ربط عقل جوجل بأمان عبر الـ Secrets
google_model = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام نموذج جيميناي الاحترافي للتحليل المعماري
    google_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    pass

engineer_name = st.text_input("اسم المهندس المعماري:")
user_prompt = st.text_area("وصف التصميم (اكتب رؤيتك المعمارية بحرية تامة):", placeholder="مثال: فيلا مودرن، واجهات بارامترية، مع إظهار مقياس المبنى بوجود أشخاص في الحديقة...")

if st.button("تشغيل النظام الذكي وتوليد التصميم ⚡", use_container_width=True):
    if not engineer_name or not user_prompt:
        st.warning("⚠️ يرجى تعبئة الحقول المطلوبة.")
    else:
        final_architectural_prompt = user_prompt
        
        # المرحلة الأولى: العقل الاستشاري (Google Gemini) للتحليل والترجمة
        if google_model:
            try:
                with st.spinner("🧠 عقل النظام يحلل الفكرة ويصيغها هندسياً..."):
                    architectural_system_instruction = """
                    You are a world-class architectural design director and senior prompt engineer.
                    Your task is to take the user's architectural description (which may be in Arabic or English) and translate/expand it into a master-level professional prompt for high-end architectural rendering engines (like Stable Diffusion 3.5 / Midjourney).
                    
                    Rules:
                    1. Maintain the user's exact creative intent without unnecessary restrictions. If they want people for scale, include architectural scale figures properly.
                    2. Add professional rendering parameters: photorealistic, 8k resolution, architectural photography, cinematic lighting, Unreal Engine 5 render, highly detailed materials, ray tracing.
                    3. Return ONLY the final English prompt text, no extra commentary or markdown formatting.
                    """
                    response = google_model.generate_content(architectural_system_instruction + "\n\nUser Description: " + user_prompt)
                    final_architectural_prompt = response.text.strip()
                    
                    # إظهار ما فعله العقل الذكي للمهندس
                    with st.expander("🔍 تفاصيل التحليل الهندسي والأوامر المطورة (اضغط للفتح)"):
                        st.code(final_architectural_prompt, language="text")
            except Exception:
                # خطة بديلة ذكية في حال توقف الـ API مؤقتاً
                final_architectural_prompt = f"{user_prompt}, professional architectural rendering, 8k resolution, photorealistic, cinematic lighting, highly detailed, Unreal Engine 5"
        else:
            final_architectural_prompt = f"{user_prompt}, professional architectural rendering, 8k resolution, photorealistic, cinematic lighting, highly detailed, Unreal Engine 5"

        # المرحلة الثانية: إرسال الأوامر لمحرك الريندر البصري
        try:
            with st.spinner("🎨 جاري بناء اللقطة المعمارية النهائية..."):
                encoded_prompt = urllib.parse.quote(final_architectural_prompt)
                
                # رابط المحرك بدقة عالية
                render_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed=999"
                
                if render_url:
                    st.success("✨ تم اكتمال الريندر بنجاح!")
                    st.image(render_url, caption=f"تصميم المهندس: {engineer_name}", use_container_width=True)
                else:
                    st.error("❌ فشل استلام الصورة من محرك الريندر.")
        except Exception as e:
            st.error(f"❌ حدث خطأ تقني أثناء التوليد: {e}")
