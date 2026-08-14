import streamlit as st
import google.generativeai as genai
import urllib.parse
import requests
import base64

# --- إعدادات النظام ---
st.set_page_config(page_title="منصة أركان المؤسسية", page_icon="🏢", layout="wide")

# استدعاء مفتاح جوجل من الأمان (Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    gemini_model = None

# --- واجهة المستخدم الاحترافية ---
st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.sidebar.header("إعدادات المشروع")

engineer_name = st.sidebar.text_input("اسم المهندس المسؤول:")
client_name = st.sidebar.text_input("اسم المشروع / العميل:")
project_type = st.sidebar.selectbox("نوع المشروع:", ["فيلا سكنية", "مجمع تجاري", "تصميم داخلي", "مبنى إداري"])
user_prompt = st.text_area("وصف الرؤية المعمارية (اكتب أفكارك):", height=150)

if st.sidebar.button("تشغيل النظام المتكامل ⚡"):
    if not all([engineer_name, client_name, user_prompt]):
        st.error("⚠️ يرجى تعبئة كافة بيانات المشروع في القائمة الجانبية.")
    else:
        # طبقة التحليل الذكي
        with st.status("جاري معالجة المشروع...", expanded=True) as status:
            final_arch_prompt = ""
            
            if gemini_model:
                st.write("🧠 تحليل العقل الذكي...")
                try:
                    analysis = gemini_model.generate_content(f"""
                    Analyze this architectural description for '{project_type}': {user_prompt}.
                    Convert into a master architectural prompt: 8k, photorealistic, Unreal Engine 5, cinematic lighting, 
                    highly detailed materials, strictly empty architectural scene, wide angle.
                    Return only the prompt.
                    """)
                    final_arch_prompt = analysis.text
                    st.write("✅ تم التحليل.")
                except:
                    final_arch_prompt = f"{project_type}, {user_prompt}, 8k, photorealistic, cinematic"
            else:
                final_arch_prompt = f"{project_type}, {user_prompt}, 8k, photorealistic"
            
            # طبقة الريندر
            st.write("🎨 جاري ريندر المشهد...")
            encoded = urllib.parse.quote(final_arch_prompt)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&seed=99"
            
            status.update(label="اكتمل العمل بنجاح!", state="complete")

        # عرض النتائج
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image(img_url, caption=f"تصميم: {client_name}", use_container_width=True)
        
        with col2:
            st.markdown("### 📋 التقرير الفني والمواصفات")
            st.success(f"""
            **مشروع:** {client_name}  
            **مهندس:** {engineer_name}  
            **الطراز:** معاصر - إقليمي  
            **الحالة:** ريندر نهائي  
            
            *ملاحظة: هذا النظام هو جزء من سلسلة ARKA-OS لتسريع دورة التصميم المعماري.*
            """)
            if st.button("تحميل التقرير"):
                st.info("سيتم تفعيل ميزة التصدير (PDF) في الخطوة القادمة.")
