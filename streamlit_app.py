import streamlit as st
import urllib.parse

st.set_page_config(page_title="منصة أركان المعمارية المؤسسية", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان المعمارية (النظام المؤسسي المتكامل)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>التحليل الهندسي البصري + إصدار التقارير الفنية التلقائية</p>", unsafe_allow_html=True)
st.divider()

engineer = st.text_input("اسم المهندس المسؤول:")
client_name = st.text_input("اسم العميل / المشروع (مثلاً: أبراج القطيبي):")
prompt = st.text_area("وصف التصميم المعماري (اكتب رؤيتك):", placeholder="مثال: فيلا مودرن بأسلوب إقليمي معاصر، واجهات بارامترية، شناشيل، مسبح عاكس...")

if st.button("تشغيل النظام المؤسسي وتوليد التصميم والتقرير ⚡", use_container_width=True):
    if not engineer or not client_name or not prompt:
        st.warning("⚠️ يرجى تعبئة جميع الحقول (اسم المهندس، اسم المشروع، ووصف التصميم).")
    else:
        with st.spinner("🔄 جاري معالجة الكتل المعمارية وصياغة المواصفات الفنية..."):
            
            # 1. هندسة الأوامر البصرية (مضمونة وخالية من أي أخطاء بشرية)
            pure_architectural_prompt = (
                f"{prompt}, professional architectural exterior visualization, "
                f"modern regionalist architecture, premium materials, glass and concrete, "
                f"ray tracing, cinematic twilight lighting, 8k resolution, ultra-photorealistic, "
                f"Unreal Engine 5 render, highly detailed, strictly empty architectural scene"
            )
            
            encoded = urllib.parse.quote(pure_architectural_prompt)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&seed=777"
            
            # عرض التصميم
            st.success("✨ تم إنجاز التصميم المعماري بنجاح!")
            st.image(img_url, caption=لفيلا / مشروع: {client_name} - تصاميم المهندس: {engineer}", use_container_width=True)
            
            st.divider()
            
            # 2. إصدار التقرير الفني والمواصفات التلقائية (الخاصية الثانية الجديدة)
            st.markdown("### 📋 التقرير الفني والمواصفات المعمارية المعتمدة")
            st.info(f"""
            * **إصدار المشروع:** نظام أركان المؤسسي (ARKA-OS)
            * **المهندس المصمم:** {engineer}
            * **العميل / الجهة المستفيدة:** {client_name}
            * **الطراز المعماري:** دمج الحداثة بالمعمار الإقليمي المعاصر.
            * **المواصفات البصرية المعتمدة:** كتل خرسانية مكشوفة، زجاج بانورامي مزدوج، معالجات تظليل هندسية، وإضاءة غسق سينمائية.
            * **الحالة:** جاهز للعرض وتقديم العروض الفنية للعملاء.
            """)
