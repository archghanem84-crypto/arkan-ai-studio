import streamlit as st
import google.generativeai as genai
import requests
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 نظام أركان المعماري (النسخة الذكية)</h1>", unsafe_allow_html=True)
st.divider()

# مفاتيح النظام
GEMINI_API_KEY = "AQ.Ab8RN6JhFsfK-Vf36xqPKE_z8K9ptqsV4EWl29k3Xecc6kgC7Q"
NVIDIA_API_KEY = "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"

genai.configure(api_key=GEMINI_API_KEY)

engineer_name = st.text_input("اسم المهندس:")
prompt = st.text_area("وصف التصميم:")

if st.button("توليد التصميم المعماري ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى إدخال البيانات.")
    else:
        st.info("🧠 1. عقل النظام يحلل الطلب ويصيغه معمارياً...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # === العقل الذكي الجديد (بدون تقييد أعمى) ===
            system_instruction = """
            أنت مهندس معماري خبير في صياغة أوامر (Prompts) لمحركات الذكاء الاصطناعي لتوليد الصور.
            مهمتك: تحويل الوصف العربي إلى وصف إنجليزي دقيق جداً واحترافي.
            
            القواعد الذكية:
            1. الموضوع الرئيسي يجب أن يكون دائماً "تصميم معماري" (مبنى، فيلا، مساحة داخلية). ابدأ الوصف دائماً بكلمات مثل: "Hyper-realistic architectural photography of..." أو "Architectural exterior visualization of...".
            2. لا تمنع وجود الأشخاص، ولكن اجعلهم دائماً عناصر ثانوية لتوضيح المقياس. استخدم مصطلحات مثل "architectural scale figures" أو "few people walking in the background". 
            3. يمنع منعاً باتاً أن يكون الوصف عن "بورتريه" أو صورة قريبة لوجه إنسان.
            4. أضف مصطلحات الريندر القوية: 8k resolution, highly detailed, photorealistic, cinematic lighting, Unreal Engine 5 style.
            5. أخرج النص الإنجليزي النهائي فقط، بدون أي شروحات إضافية.
            """
            
            response = model.generate_content(system_instruction + "\nوصف المستخدم: " + prompt)
            arch_prompt = response.text.strip()
            
            with st.expander("🔍 شاهد التحليل الهندسي والأوامر (اضغط للفتح)"):
                st.write(arch_prompt)
                
            st.info("🎨 2. جاري التوليد عبر محرك NVIDIA القوي (Stable Diffusion 3.5)...")
            
            invoke_url = "https://integrate.api.nvidia.com/v1/images/generations"
            headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"}
            
            # استخدمنا فلتر سلبي (Negative Prompt) ذكي يمنع الوجوه القريبة (البورتريه) والتشوهات فقط
            payload = {
                "model": "stabilityai/stable-diffusion-3-5-large",
                "prompt": arch_prompt,
                "negative_prompt": "portrait, close-up face, character design, blurry, low quality, deformed structure, poorly drawn architecture",
                "aspect_ratio": "16:9"
            }
            
            response = requests.post(invoke_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                img_b64 = data.get('data', [{}])[0].get('b64_json')
                if img_b64:
                    st.success("✨ تم التوليد بنجاح!")
                    st.image(base64.b64decode(img_b64), caption=f"تصميم المهندس: {engineer_name}", use_column_width=True)
                else:
                    st.error("لم يتم استلام الصورة من الخادم.")
            else:
                st.error(f"خطأ الاتصال بـ NVIDIA: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
