import streamlit as st
import google.generativeai as genai
import urllib.parse

# إعدادات الصفحة الاحترافية لمنصة أركان
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>نظام الذكاء الاصطناعي المدمج (التحليل الهندسي + التوليد البصري)</p>", unsafe_allow_html=True)
st.divider()

# مفتاح Google AI Studio الخاص بالمنصة
GEMINI_API_KEY = "AQ.Ab8RN6JhFsfK-Vf36xqPKE_z8K9ptqsV4EWl29k3Xecc6kgC7Q"
genai.configure(api_key=GEMINI_API_KEY)

# واجهة المهندس
engineer_name = st.text_input("اسم المهندس المعماري:", placeholder="أدخل اسمك هنا...")
prompt = st.text_area(
    "وصف التصميم المعماري (اكتب أفكارك بالعربية براحتك):", 
    placeholder="مثال: فيلا مودرن بأسلوب إقليمي معاصر، واجهات بارامترية تدمج الشناشيل الخشبية، طيرمانة زجاجية حديثة، إضاءة ليلية دافئة..."
)

if st.button("تحليل هندسي وتوليد التصميم ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى كتابة اسم المهندس ووصف التصميم لتبدأ المنصة عملها.")
    else:
        try:
            # =====================================================================
            # المرحلة الأولى: العقل الذكي (Google Gemini) للتحليل والترجمة الهندسية
            # =====================================================================
            st.info("🧠 1. يقوم عقل النظام الآن بتحليل فكرتك وتحويلها لأوامر هندسية دقيقة...")
            
            # استدعاء أسرع وأذكى نموذج من جوجل
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # برمجة شخصية الذكاء الاصطناعي ليكون خبيراً معمارياً متوافقاً مع أسلوب التصميم
            system_instruction = """
            أنت مهندس معماري محترف وخبير عالمي في كتابة أوامر (Prompts) دقيقة لبرامج الريندر والذكاء الاصطناعي.
            المستخدم سيعطيك فكرة تصميم باللغة العربية. مهمتك هي تحويل هذه الفكرة إلى وصف إنجليزي دقيق جداً واحترافي لتوليد صورة معمارية واقعية.
            
            القواعد الصارمة التي يجب اتباعها:
            1. استخدم مصطلحات ريندر قوية مثل: Hyper-realistic, 8k resolution, Unreal Engine 5 render, architectural photography, highly detailed, ray tracing.
            2. ركز على الإضاءة (مثل cinematic lighting, twilight, golden hour).
            3. إذا ذكر المستخدم عناصر إقليمية مثل "طيرمانة" ترجمها إلى "modern glass-enclosed rooftop pavilion (Tayramana)". وإذا ذكر "شناشيل" ترجمها إلى "intricate wooden bay windows (Shanashil) and geometric breeze blocks".
            4. هام جداً جداً: يجب أن تضيف في نهاية الوصف هذه الجملة حرفياً لمنع ظهور أي أشخاص: "No people, strictly empty architectural scene, unpopulated".
            5. أخرج فقط الوصف الإنجليزي النهائي. لا تكتب أي مقدمات، لا تكتب شروحات، ولا تقل "Here is the prompt". فقط الوصف.
            """
            
            # معالجة النص
            response = model.generate_content(system_instruction + "\n\nوصف المهندس بالعربية:\n" + prompt)
            enhanced_english_prompt = response.text.strip()
            
            st.success("✅ اكتمل التحليل الهندسي! تم تجهيز أوامر الريندر الاحترافية.")
            
            # عرض الوصف الإنجليزي للمهندس ليرى كيف تطورت فكرته
            with st.expander("🔍 شاهد الأوامر الهندسية التي كتبها النظام لمحرك الريندر (اضغط للفتح)"):
                st.code(enhanced_english_prompt, language="text")
            
            # =====================================================================
            # المرحلة الثانية: محرك التوليد البصري لرسم الصورة
            # =====================================================================
            st.info("🎨 2. جاري تحويل الأوامر الهندسية إلى تحفة معمارية بصرية...")
            
            # تحويل النص ليكون متوافقاً مع روابط الويب
            encoded_prompt = urllib.parse.quote(enhanced_english_prompt)
            
            # استدعاء محرك الصور الفوري للحصول على ريندر عالي الدقة
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            
            # عرض النتيجة النهائية المبهرة
            st.success(f"✨ اكتملت العملية بنجاح للمهندس {engineer_name}!")
            st.image(image_url, caption=f"تصميم المهندس: {engineer_name} | (تمت المعالجة والتحليل عبر عقل المنصة الذكي)", use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ حدث خطأ غير متوقع في النظام: {e}")
