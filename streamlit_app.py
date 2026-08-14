import streamlit as st
import requests
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>نظام التصميم المعماري المتكامل المربوط بالسحابة</p>", unsafe_allow_html=True)

st.divider()

# المفتاح السري مدمج في الكود (مخفي تماماً عن المستخدمين)
NVIDIA_API_KEY = "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"

# مدخلات المهندس (واجهة نظيفة وبسيطة)
engineer_name = st.text_input("اسم المهندس المعماري:")
prompt = st.text_area("وصف التصميم المعماري المطلوب (Prompt):", placeholder="مثال: فيلا مودرن بأسلوب إقليمي معاصر، واجهات بارامترية مع شناشيل، إضاءة ليلية، 8k...")

if st.button("توليد التصميم وحفظه في الذاكرة ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى كتابة اسم المهندس ووصف التصميم أولاً.")
    else:
        st.info("🔄 جاري إرسال الطلب إلى محركات الذكاء الاصطناعي...")
        
        try:
            # إعداد طلب الاتصال بمحرك إنفيديا للتوليد البصري
            invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-medium"
            headers = {
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Accept": "application/json",
            }
            payload = {
                "prompt": prompt + ", luxury architectural photography, highly detailed, photorealistic, 8k resolution",
                "cfg_scale": 5,
                "aspect_ratio": "16:9",
                "seed": 0,
                "steps": 25,
                "negative_prompt": "blurry, low quality, distorted, watermark"
            }

            response = requests.post(invoke_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                image_base64 = data.get('image')
                
                if image_base64:
                    # تحويل الصورة إلى صيغة قابلة للعرض
                    image_bytes = base64.b64decode(image_base64)
                    st.success("✨ تم معالجة الطلب وتوليد التصميم بنجاح!")
                    st.image(image_bytes, caption=f"تصميم المهندس: {engineer_name}", use_container_width=True)
                else:
                    st.error("❌ تم الاتصال ولكن لم يتم استرجاع الصورة. حاول تعديل الوصف.")
            else:
                st.error(f"❌ خطأ في الاتصال بالمحرك: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ حدث خطأ تقني: {e}")
