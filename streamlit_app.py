import streamlit as st
import google.generativeai as genai
import urllib.parse

st.set_page_config(page_title="منصة أركان المعمارية", layout="centered")
st.title("🏢 منصة أركان المعمارية")

# جلب المفتاح بأمان
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    google_connected = True
except:
    google_connected = False

engineer = st.text_input("اسم المهندس:")
prompt = st.text_area("وصف التصميم:")

if st.button("توليد التصميم"):
    if not prompt:
        st.warning("يرجى كتابة وصف.")
    else:
        final_prompt = prompt
        
        # 1. محاولة التحسين عبر جوجل
        if google_connected:
            try:
                with st.spinner("جاري التحسين الهندسي..."):
                    res = model.generate_content(f"حول هذا الوصف إلى وصف إنجليزي معماري احترافي (8k, photorealistic): {prompt}")
                    final_prompt = res.text
                    st.success("تم التحسين.")
            except:
                st.warning("تعذر الاتصال بعقل جوجل، استخدمت الوصف المباشر.")
        
        # 2. توليد الصورة (بأمان)
        try:
            with st.spinner("جاري توليد الصورة..."):
                encoded = urllib.parse.quote(final_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=675&nologo=true"
                
                # شرط الحماية (إذا لم يوجد رابط لا تعرض)
                if img_url:
                    st.image(img_url, caption=f"تصميم: {engineer}", use_column_width=True)
                else:
                    st.error("فشل توليد الصورة.")
        except Exception as e:
            st.error(f"خطأ في الريندر: {e}")
