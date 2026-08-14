import streamlit as st
import google.generativeai as genai
import urllib.parse
import requests
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 نظام أركان المعماري (النسخة النهائية)</h1>", unsafe_allow_html=True)
st.divider()

# مفتاح جوجل
GEMINI_API_KEY = "AQ.Ab8RN6JhFsfK-Vf36xqPKE_z8K9ptqsV4EWl29k3Xecc6kgC7Q"

# تهيئة جوجل بمرونة أكبر
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في تهيئة جوجل: {e}")

engineer_name = st.text_input("اسم المهندس:")
prompt = st.text_area("وصف التصميم المعماري (اكتب بالعربية):", placeholder="مثال: فيلا مودرن...")

if st.button("توليد التصميم المعماري ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى إدخال البيانات.")
    else:
        st.info("🧠 1. جاري التحليل الهندسي...")
        final_prompt = ""
        
        # محاولة التحليل عبر جوجل
        try:
            instruction = """
            أنت مهندس معماري خبير. حول هذا الوصف العربي إلى وصف إنجليزي دقيق للتصميم المعماري.
            التركيز على: Hyper-realistic, 8k, architectural visualization, cinematic lighting.
            لا تحذف الأشخاص تماماً، اجعلهم عناصر ثانوية للمقياس. 
            أعطني فقط النص الإنجليزي.
            """
            response = model.generate_content(instruction + "\nوصف المستخدم: " + prompt)
            final_prompt = response.text.strip()
            st.success("✅ تم التحليل بنجاح.")
        except Exception as e:
            # الخطة البديلة: إذا فشل جوجل، نستخدم الوصف العربي كما هو كـ Prompt
            st.warning("⚠️ تعذر الاتصال بعقل جوجل، سأستخدم الوصف المباشر للمحرك.")
            final_prompt = prompt + ", hyper-realistic architectural rendering, 8k, cinematic lighting"

        # توليد الصورة
        st.info("🎨 2. جاري الريندر...")
        encoded_prompt = urllib.parse.quote(final_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed=42"
        
        st.image(image_url, caption=f"تصميم: {engineer_name}", use_column_width=True)
        st.success("✨ تم التوليد!")
