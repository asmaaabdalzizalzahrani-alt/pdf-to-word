
# Online Python - IDE, Editor, Compiler, Interpreter
import os
import tempfile
from pathlib import Path

import streamlit as st
from pdf2docx import Converter

# استخدمي كلمة مرور أقوى في الإنتاج وليس نصًا ثابتًا
PASSWORD = "12345"

st.set_page_config(page_title="محول PDF الخاص", page_icon="🔒", layout="centered")


def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    with st.form("login_form", clear_on_submit=False):
        password = st.text_input("أدخل كلمة المرور لدخول الموقع:", type="password", key="password")
        submitted = st.form_submit_button("دخول")

        if submitted:
            if password == PASSWORD:
                st.session_state["password_correct"] = True
            else:
                st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.warning("😕 كلمة المرور غير صحيحة، حاول مرة أخرى.")
    return False


if not check_password():
    st.stop()

st.title("📄 محول ملفات PDF إلى Word (خاص)")
st.write("مرحباً بكِ! هذا الموقع محمي ولا يراه إلا من يحمل كلمة المرور.")

uploaded_file = st.file_uploader("اختر ملف PDF", type=["pdf"])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_pdf_path = os.path.join(tmp_dir, "input.pdf")
        output_docx_path = os.path.join(tmp_dir, "converted.docx")

        with open(input_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            with st.spinner("جاري تحويل الملف..."):
                cv = Converter(input_pdf_path)
                cv.convert(output_docx_path, start=0, end=None)
                cv.close()

            st.success("تم التحويل بنجاح! 🎉")

            docx_bytes = Path(output_docx_path).read_bytes()
            st.download_button(
                label="⬇️ تحميل ملف Word",
                data=docx_bytes,
                file_name=uploaded_file.name.replace(".pdf", ".docx"),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            


