import streamlit as st
import requests
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة أركان المعمارية الذكية", page_icon="🏢", layout="centered")

st.markdown("<h1 style='text-align: center; color: #10b981;'>🏢 منصة أركان للاستوديو المعماري الذكي</h1>", unsafe_allow_html=True)
st.divider()

# المفتاح الذي تم فحصه ونجح
NVIDIA_API_KEY = "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"

engineer_name = st.text_input("اسم المهندس المعماري:")
prompt = st.text_area("وصف التصميم المعماري (Prompt):", placeholder="مثال: فيلا مودرن بأسلوب إقليمي معاصر...")

if st.button("توليد التصميم ⚡", use_container_width=True):
    if not engineer_name or not prompt:
        st.warning("⚠️ يرجى تعبئة الحقول.")
    else:
        st.info("🔄 1. جاري فحص حسابك واختيار أفضل نموذج صور متاح...")
        
        try:
            # 1. جلب النماذج المتاحة
            headers_models = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json"}
            models_resp = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers_models)
            
            if models_resp.status_code == 200:
                models_data = models_resp.json().get("data", [])
                model_ids = [m.get("id") for m in models_data]
                
                # البحث عن نموذج صور في حسابك (Stability أو Flux)
                target_model = None
                for m in model_ids:
                    if "stability" in m.lower() or "flux" in m.lower():
                        target_model = m
                        break
                        
                if target_model:
                    st.success(f"✅ تم العثور على النموذج المدعوم لحسابك: {target_model}")
                    st.info("🔄 2. جاري توليد التصميم الآن (قد يستغرق 10-20 ثانية)...")
                    
                    # 2. توليد الصورة بالمسار الموحد
                    gen_url = "https://integrate.api.nvidia.com/v1/images/generations"
                    headers_gen = {
                        "Authorization": f"Bearer {NVIDIA_API_KEY}", 
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                    payload = {
                        "model": target_model,
                        "prompt": prompt + ", professional architectural photography, hyper-realistic, 8k",
                        "response_format": "b64_json"
                    }
                    
                    gen_resp = requests.post(gen_url, headers=headers_gen, json=payload)
                    
                    if gen_resp.status_code == 200:
                        img_b64 = gen_resp.json().get('data', [{}])[0].get('b64_json')
                        if img_b64:
                            st.success("✨ تم التوليد بنجاح!")
                            st.image(base64.b64decode(img_b64), caption=f"تصميم: {engineer_name}", use_container_width=True)
                        else:
                            st.error("❌ لم نجد بيانات الصورة في الرد.")
                            
                    elif gen_resp.status_code == 404:
                        st.warning("⚠️ المسار الموحد أعطى 404، جاري تجربة المسار المباشر الخاص بنيفيديا...")
                        # المسار الاحتياطي في حال كان النموذج يستخدم مساراً قديماً
                        gen_url_fallback = f"https://ai.api.nvidia.com/v1/genai/{target_model}"
                        payload_fallback = {
                            "prompt": prompt + ", professional architectural photography, hyper-realistic, 8k",
                            "aspect_ratio": "16:9",
                        }
                        resp_fall = requests.post(gen_url_fallback, headers=headers_gen, json=payload_fallback)
                        
                        if resp_fall.status_code == 200:
                            data_fall = resp_fall.json()
                            img_b64_fall = data_fall.get('image') or data_fall.get('artifacts', [{}])[0].get('base64')
                            if img_b64_fall:
                                st.success("✨ تم التوليد بنجاح بالمسار المباشر!")
                                st.image(base64.b64decode(img_b64_fall), caption=f"تصميم: {engineer_name}", use_container_width=True)
                            else:
                                st.error("❌ الرد لم يحتوي على صورة.")
                        else:
                            st.error(f"❌ فشل التوليد حتى بالمسار الاحتياطي: {resp_fall.status_code} - {resp_fall.text}")
                    else:
                        st.error(f"❌ خطأ في التوليد: {gen_resp.status_code} - {gen_resp.text}")
                else:
                    st.error("❌ حسابك متصل بنجاح، لكن لم نجد نماذج صور مفعلة. يرجى التأكد من تفعيلها في موقع نيفيديا.")
            else:
                st.error(f"❌ خطأ في جلب النماذج: {models_resp.status_code}")
                
        except Exception as e:
            st.error(f"❌ خطأ تقني في الموقع: {e}")
