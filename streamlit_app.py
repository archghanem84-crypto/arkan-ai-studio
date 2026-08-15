import streamlit as st
import requests
import base64
import urllib.parse

# --- إعدادات النظام المؤسسي المتقدم ---
st.set_page_config(page_title="ARKA-OS Enterprise | Pro Studio", layout="wide")
st.title("🏢 ARKA-OS | استوديو التصميم المعماري المتطور")

# سحب المفتاح بأمان
gemini_key = st.secrets.get("GEMINI_API_KEY", "")

# --- الشريط الجانبي للخصائص المعمارية (Sidebar) ---
st.sidebar.header("🛠️ إعدادات الكتلة والتشطيب")
engineer = st.sidebar.text_input("اسم المهندس المشرف:", value="محمد غانم")
project_name = st.sidebar.text_input("اسم المشروع المعماري:", value="مشروع فيلا")

# الخائص التفصيلية الجديدة
floors = st.sidebar.selectbox("عدد الأدوار والمستويات:", ["دور واحد (Ground Floor)", "دورين (G+1)", "ثلاثة أدوار (G+2)", "برج / متعدد الأدوار"])
finishing_type = st.sidebar.selectbox("طراز التشطيب الخارجي:", ["حجر طبيعي دافئ مع زجاج ممتد", "خرسانة معاصرة وبلوك مفرغ (بريز بلوك)", "تراثي إقليمي مع شناشيل وطيرمانة", "مودرن نقي بكتل بيضاء ملساء"])
lighting_style = st.sidebar.selectbox("نوع الإضاءة والجو العام:", ["إضاءة ليلية سينمائية دافئة", "إضاءة نهارية طبيعية ساطعة", "إضاءة غروب الشمس (Golden Hour)"])
render_style = st.sidebar.selectbox("مستوى التفاصيل والواقعية:", ["واقعي فائق الجودة (Photorealistic 8K)", "منظور هندسي معماري (Architectural Blueprint Style)"])

# --- واجهة الإدخال الرئيسية ---
user_input = st.text_area("وصف الرؤية المعمارية الإضافية (موقع، تفاصيل خاصة...):", placeholder="اكتب ملاحظاتك الإضافية هنا...")

if st.button("🚀 تنفيذ الريندر المعماري المؤسسي المتكامل"):
    if not user_input or not gemini_key:
        st.warning("⚠️ يرجى التأكد من كتابة الوصف المعماري ووجود مفتاح Gemini في الـ Secrets.")
    else:
        with st.status("جاري دمج خصائص الشريط الجانبي وهندسة البرومبت الشامل...", expanded=True) as status:
            
            # 1. دمج مدخلات الشريط الجانبي أوتوماتيكياً مع وصف المستخدم وإرسالها لـ Gemini
            st.write("🧠 دمج المتغيرات وهندسة البرومبت الاحترافي...")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            
            combined_prompt_context = (
                f"User Concept: {user_input}. "
                f"Architectural Specifications -> Floors: {floors}, Finishing & Materials: {finishing_type}, "
                f"Lighting & Atmosphere: {lighting_style}, Style: {render_style}."
            )
            
            system_instruction = (
                f"You are a master chief architectural design director. "
                f"Analyze these parameters: '{combined_prompt_context}'. "
                f"Build an elite, highly detailed professional English architectural exterior render prompt incorporating all specified materials, floors, and lighting style. "
                f"STRICT RULE: Focus ONLY on building structure and facade. NEVER generate human figures, portraits, or faces. "
                f"Also provide a detailed technical engineering report in Arabic covering structural breakdown and material selection. "
                f"Format strictly as: PROMPT: [Detailed English Prompt] | REPORT: [Detailed Arabic Report]"
            )
            
            gemini_payload = {
                "contents": [{"parts": [{"text": system_instruction}]}]
            }
            
            p_part = f"{combined_prompt_context}, professional architectural exterior building rendering, ultra-detailed facade, 8k resolution, photorealistic, cinematic lighting, Unreal Engine 5"
            r_part = f"مشروع ({project_name}): تم دمج خيارات ({floors}) مع تشطيب ({finishing_type}) وإضاءة ({lighting_style})."
            
            try:
                gemini_resp = requests.post(gemini_url, json=gemini_payload, timeout=25).json()
                analysis_text = gemini_resp['candidates'][0]['content']['parts'][0]['text']
                if "|" in analysis_text:
                    p_part = analysis_text.split('|')[0].replace("PROMPT:", "").strip()
                    r_part = analysis_text.split('|')[1].replace("REPORT:", "").strip()
            except Exception:
                pass

            # عرض البرومبت الهندسي المعتمد
            st.info(f"🔍 **البرومبت الهندسي المدمج:** {p_part}")

            # 2. التوليد البصري الفوري
            st.write("🎨 إصدار اللقطة المعمارية النهائية...")
            encoded_prompt = urllib.parse.quote(p_part)
            img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed=202"
            
            try:
                img_resp = requests.get(img_url, timeout=45)
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
                    st.error("حدث خطأ أثناء استقبال الريندر.")
            except Exception as e:
                status.update(label="خطأ شبكي", state="error")
                st.error(f"فشل الاتصال: {e}")
