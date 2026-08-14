import streamlit as st
import google.generativeai as genai
import urllib.parse

st.set_page_config(page_title="منصة أركان المعمارية", layout="centered")
st.title("🏢 منصة أركان المعمارية")

# محاولة الاتصال بجوجل
google_connected = False
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    google_connected = True
except Exception:
    pass

engineer = st.text_input("اسم المهندس:")
prompt = st.text_area("وصف التصميم:")

if st.button("توليد التصميم المعماري ⚡"):
    if not prompt:
        st.warning("يرجى كتابة وصف.")
    else:
        final_prompt = prompt
        
        # 1. المعالجة الذكية
        if google_connected:
            try:
                with st.spinner("جاري التحسين الهندسي عبر الذكاء الاصطناعي..."):
                    res = model.generate_content(f"Translate this architectural description to English and enhance it with professional rendering keywords (8k, photorealistic, cinematic lighting, Unreal Engine 5). Keep scale figures if mentioned but make them secondary: {prompt}")
                    final_prompt = res.text
                    st.success("تم التحسين بنجاح.")
            except:
                # تفعيل المعالج الاحتياطي المضخم في حال انقطاع الشبكة
                st.warning("تم تفعيل المعالج المعماري الاحتياطي.")
                final_prompt = f"{prompt}, hyper-realistic architectural rendering, 8k resolution, photorealistic, cinematic twilight lighting, highly detailed, Unreal Engine 5, architectural scale figures"
        else:
            st.warning("تم تفعيل المعالج المعماري الاحتياطي.")
            final_prompt = f"{prompt}, hyper-realistic architectural rendering, 8k resolution, photorealistic, cinematic twilight lighting, highly detailed, Unreal Engine 5, architectural scale figures"
        
        # 2. توليد وعرض الصورة
        try:
            with st.spinner("جاري بناء اللقطة المعمارية..."):
                encoded = urllib.parse.quote(final_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true"
                
                if img_url:
                    # تم إصلاح الخطأ الجذري هنا
                    st.image(img_url, caption=f"تصميم: {engineer}", use_container_width=True)
                else:
                    st.error("فشل توليد الصورة.")
        except Exception as e:
            st.error(f"خطأ في الريندر: {e}")
