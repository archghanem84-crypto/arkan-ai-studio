import streamlit as st
import requests

st.set_page_config(page_title="أداة التشخيص", layout="centered")
st.title("أداة فحص الاتصال بـ NVIDIA")

# مفتاحك
NVIDIA_API_KEY = "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"

if st.button("فحص الاتصال واستخراج النماذج المتاحة"):
    st.info("جاري فحص الحساب...")
    try:
        # هذا الرابط يسرد كل النماذج المتاحة لك
        url = "https://integrate.api.nvidia.com/v1/models"
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            st.success("تم الاتصال بنجاح!")
            data = response.json()
            # عرض النماذج المتاحة
            st.write("النماذج المتاحة في حسابك:")
            st.json(data) 
        else:
            st.error(f"خطأ {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"خطأ تقني: {e}")
