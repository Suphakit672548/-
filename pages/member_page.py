import streamlit as st
import model
import controller


# =========================
# View helpers (reset form)
# =========================
def reset_member_form():
    st.session_state["member_code"] = ""
    st.session_state["member_name"] = ""
    st.session_state["gender"] = "ไม่ระบุ"
    st.session_state["member_email"] = ""
    st.session_state["member_phone"] = ""
    # st.session_state["is_active"] = True


# =========================
# UI
# =========================


def render_member():

    st.header("🧍‍♂️ สมัครสมาชิกใหม่")

    with st.form("add_member_form"):
        col1, col2 = st.columns(2)

        with col1:
            member_code = st.text_input(
                "รหัสสมาชิก",
                key="member_code"
            )
            member_name = st.text_input(
                "ชื่อ - สกุล",
                key="member_name"
            )
            gender = st.selectbox(
                "เพศ",
                ["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"],
                key="gender"
            )

        with col2:
            email = st.text_input(
                "อีเมล",
                key="member_email"
            )
            phone = st.text_input(
                "เบอร์โทรศัพท์",
                key="member_phone"
            )

        submitted = st.form_submit_button("บันทึกสมาชิก")

    if submitted:
        success, result = controller.create_member(
            member_code,
            member_name,
            gender,
            email,
            phone
        )

        if success:
            st.success(result)
            reset_member_form()
            st.rerun()
        else:
            for err in result:
                st.error("⚠ " + err)

    # =========================
    # LIST MEMBERS
    # =========================

    st.subheader("📋 รายชื่อสมาชิกทั้งหมด")

    members_df = model.get_all_members()

    if members_df.empty:
        st.info("ยังไม่มีข้อมูลสมาชิก")
        return

    for _, row in members_df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 3, 2, 1])

        with col1:
            st.write(f"**{row['member_code']}** : {row['name']}")

        with col2:
            st.write(row["email"] if row["email"] else "-")

        with col3:
            st.write("ใช้งาน" if row["is_active"] else "ยกเลิก")

        with col4:
            if st.button("ลบ", key=f"delete_{row['id']}"):
                controller.remove_member(row["id"])
                st.success("ลบสมาชิกแล้ว")
                st.rerun()

    # =========================
    # EDIT MEMBER
    # =========================

    st.subheader("✏️ แก้ไขข้อมูลสมาชิก")

    member_options = [
        f"{row['id']} - {row['member_code']} : {row['name']}"
        for _, row in members_df.iterrows()
    ]

    selected = st.selectbox("เลือกสมาชิก", member_options)
    selected_id = int(selected.split(" - ")[0])

    selected_row = members_df[members_df["id"] == selected_id].iloc[0]

    with st.form("edit_member_form"):
        col1, col2 = st.columns(2)

        with col1:
            edit_code = st.text_input(
                "รหัสสมาชิก",
                value=selected_row["member_code"]
            )
            edit_name = st.text_input(
                "ชื่อ - สกุล",
                value=selected_row["name"]
            )
            edit_gender = st.selectbox(
                "เพศ",
                ["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"],
                index=["ไม่ระบุ", "หญิง", "ชาย", "อื่น ๆ"].index(
                    selected_row["gender"] or "ไม่ระบุ"
                )
            )

        with col2:
            edit_email = st.text_input(
                "อีเมล",
                value=selected_row["email"] or ""
            )
            edit_phone = st.text_input(
                "เบอร์โทรศัพท์",
                value=selected_row["phone"] or ""
            )
            edit_active = st.checkbox(
                "ยังใช้งานอยู่",
                value=bool(selected_row["is_active"])
            )

        updated = st.form_submit_button("บันทึกการแก้ไข")

    if updated:
        success, result = controller.update_member(
            member_id=selected_id,
            member_code=edit_code,
            name=edit_name,
            gender=edit_gender,
            email=edit_email,
            phone=edit_phone,
            is_active=edit_active,
            old_member_code=selected_row["member_code"],
            old_email=selected_row["email"] or ""
        )

        if success:
            st.success(result)
            st.rerun()
        else:
            for err in result:
                st.error("⚠ " + err)
