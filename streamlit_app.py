import streamlit as st
import requests
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>النظام المؤسسي التراكمي المربوط بالسحابة</p>", unsafe_allow_html=True)
st.divider()

# مفتاحك السري الجديد (مفعل ونشط)
NVIDIA_API_KEY = "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"

# مدخلات المهندس
engineer_name = st.text_input("اسم المهندس المعماري:")
prompt = st.text_area("وصف التصميم المعماري (Prompt):", placeholder="مثال: فيلا مودرن بأسلوب يمني، طيرمانة حديثة، إضاءة ليلية...")

if st.button("توليد التصميم ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى تعبئة الحقول.")
    else:
        st.info("🔄 جاري إرسال الطلب لمحرك NVIDIA الذكي...")
        
        try:
            # الرابط المباشر للنموذج الذي قمت بتفعيله
            invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-3-5-large"
            
            headers = {
                "Authorization": f"Bearer {NVIDIA_API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            
            payload = {
                "prompt": prompt + ", architectural photography, hyper-realistic, 8k resolution",
                "cfg_scale": 5,
                "aspect_ratio": "16:9",
                "seed": 0,
                "steps": 25,
                "negative_prompt": "blurry, low quality, distorted"
            }

            response = requests.post(invoke_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                image_base64 = data.get('image')
                
                if image_base64:
                    image_bytes = base64.b64decode(image_base64)
                    st.success("✨ تم توليد التصميم بنجاح!")
                    st.image(image_bytes, caption=f"تصميم: {engineer_name}", use_column_width=True)
                else:
                    st.error("❌ لم يتم استرجاع الصورة من الخادم.")
            else:
                st.error(f"❌ خطأ في الاتصال: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"❌ حدث خطأ تقني: {e}")
