import streamlit as st


from pages import book_page
from pages import member_page
from pages import borrow_page
from pages import login_page
from pages import admin_page
from pages import report_page

# =========================
# LOGIN GATE
# =========================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    login_page.render_login()
    st.stop()   # ⛔ หยุดไม่ให้ไปหน้าอื่น

# =========================
# View helpers (reset form)
# =========================


# ซ่อนเมนูอัตโนมัติ (app/book page/...)
# ✅ ซ่อน Multi-page auto nav (Streamlit sidebar pages list) + fallback หลาย selector
st.markdown("""
<style>
/* 1) ตัวหลัก: Sidebar navigation ของ multipage */
section[data-testid="stSidebarNav"] {display: none !important;}


/* 2) fallback: เผื่อ DOM เปลี่ยนชื่อ/โครง */
div[data-testid="stSidebarNav"] {display: none !important;}
nav[data-testid="stSidebarNav"] {display: none !important;}


/* 3) fallback เพิ่มเติม: ซ่อนหัวข้อ Pages / รายการหน้า (บางเวอร์ชัน) */
div[data-testid="stSidebarNavItems"] {display: none !important;}
div[data-testid="stSidebarNavSeparator"] {display: none !important;}


/* 4) fallback สุดท้าย: ถ้า Streamlit render เป็น <ul>/<li> ใน sidebar */
aside ul:has(a[href*="?page="]) {display: none !important;}
aside ul:has(a[href*="/book_page"]) {display: none !important;}
aside ul:has(a[href*="/member_page"]) {display: none !important;}
aside ul:has(a[href*="/borrow_page"]) {display: none !important;}
</style>
""", unsafe_allow_html=True)
# =========================
# UI
# =========================
st.set_page_config(page_title="ระบบยืม-คืนหนังสือ", page_icon="📚")
st.title("📚 ระบบยืม-คืนหนังสือ (Streamlit + SQLite)")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (ปรับโครงสร้างแบบ MVC เชิงแนวคิด)")


# menu = st.sidebar.radio("เมนู", ["📚 หนังสือ", "👤 สมาชิก", "🔄 ยืม-คืน"])
# if menu == "📚 หนังสือ":
#     book_page.render_book()
# elif menu == "👤 สมาชิก":
#     member_page.render_member()
# else:
#     borrow_page.render_borrow()


# ---------- เมนูแบบคลิกแถบ ----------
if "page" not in st.session_state:
    st.session_state.page = "books"


# --- เมนู ---

# ===== Sidebar Menu Title (Centered & Styled) =====
st.sidebar.markdown("""
<style>
.menu-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>


<div class="menu-title">
    เมนู
</div>
""", unsafe_allow_html=True)

# =========================
# USER INFO + LOGOUT
# =========================
st.sidebar.divider()

user = st.session_state.get("user")
role = user["role"] if user else None

if user:
    st.sidebar.markdown(
        f"👤 **{user['username']}**  \n🛡️ role: `{role}`"
    )
if st.sidebar.button("🚪 ออกจากระบบ", use_container_width=True):
    st.session_state.clear()
    st.rerun()

def nav_button(label, key, icon=""):
    active = (st.session_state.page == key)
    btn = st.sidebar.button(f"{icon} {label}", use_container_width=True, key=f"btn_{key}")
    if btn:
        st.session_state.page = key
        st.rerun()
    # ทำไฮไลต์แบบง่าย (ตัวหนา/ตัวชี้)
    # if active:
    #     st.sidebar.markdown(f"✅ **{label}**")


nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")
# ✅ เพิ่มเติม: เมนูจัดการผู้ใช้ เฉพาะ admin เท่านั้น
if role == "admin":
     nav_button("จัดการผู้ใช้", "admin", "🛠️")

 # ---------- Routing ----------
# ✅ แก้ไขใหม่: ป้องกัน staff เข้าหน้า admin ด้วยการบังคับ routing
# ✅ แก้ไขใหม่: เอาการบังคับ staff ไปหน้า borrows ออก (เพราะ staff ทำได้ทุกอย่างแล้ว)


if st.session_state.page == "books":
    book_page.render_book()


elif st.session_state.page == "members":
    member_page.render_member()
elif st.session_state.page == "borrows":
    borrow_page.render_borrow()
elif st.session_state.page == "reports":
    report_page.render_report()

elif st.session_state.page == "admin":
    # ✅ เพิ่มเติม: guard กัน staff เข้าหน้า admin แม้พยายามเปลี่ยน state เอง
    if role != "admin":
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        admin_page.render_admin()
else:
    # fallback
    book_page.render_book()

nav_button("รายงาน", "reports", "📊")

