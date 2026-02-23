import streamlit as st
import controller


def render_login():
    st.title("🔐 เข้าสู่ระบบ")
            
        # -------------------------------
    # ส่วนแสดงข้อมูลผู้จัดทำ (เรียบ ชัด ชิดซ้าย)
    # -------------------------------
    st.markdown("---")

    st.markdown("### 👨‍💻 ผู้จัดทำ")

    st.markdown("""
    <div style="font-size:18px; line-height:1.8;">
    <b>ชื่อ-สกุล:</b> นาย ศุภกิจ หัตภาภรณ์เนรมิต
    <b>รหัสนักศึกษา:</b>  6740259117
    <b>หมู่เรียน:</b> ว.6706
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น admin")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="เช่น 1234")
        submitted = st.form_submit_button("Login")

    if submitted:
        ok, msgs, user_info = controller.login(username, password)
        if not ok:
            for m in msgs:
                st.error(m)
        else:
            for m in msgs:
                st.success(m)

            st.session_state["is_logged_in"] = True
            st.session_state["user"] = user_info
            st.session_state["page"] = "books"  # หรือให้ไป borrows ก็ได้
            st.rerun()

   