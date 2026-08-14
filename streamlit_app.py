import streamlit as st
import urllib.parse

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>النظام المؤسسي التراكمي المربوط بالسحابة</p>", unsafe_allow_html=True)
st.divider()

# مدخلات المهندس
engineer_name = st.text_input("اسم المهندس المعماري:")
prompt = st.text_area("وصف التصميم المعماري (Prompt):", placeholder="مثال: فيلا مودرن بأسلوب عربي، واجهات بارامترية، إضاءة ليلية، 8k...")

if st.button("توليد التصميم ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى تعبئة الحقول.")
    else:
        st.info("🔄 جاري معالجة البيانات وتوليد التصميم المعماري...")
        
        try:
            # إضافة كلمات مفتاحية معمارية احترافية لزيادة دقة الريندر
            enhanced_prompt = f"{prompt}, professional architectural photography, hyper-realistic, highly detailed, 8k resolution, photorealistic"
            
            # تحويل النص ليكون متوافقاً مع الروابط
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # استخدام محرك توليد الصور المفتوح (يعمل فوراً بدون مفتاح)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            
            # عرض النتيجة
            st.success("✨ تم توليد التصميم بنجاح!")
            st.image(image_url, caption=f"تصميم المهندس: {engineer_name}", use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء عرض الصورة: {e}")
