import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ---------------- CONFIG ----------------
ADMIN_PHONE = "919392540435"
DATA_FILE = "users_db.json"

EMERGENCY_CONTACTS = {
    "Police": "100",
    "Ambulance": "108",
    "Fire": "101",
    "Yuva Shakti Leader": "919392540435",
    "Local Volunteer": "9381981220"
}

PROGRAMS = [
    {
        "title": "Career Guidance Program",
        "desc": "Guidance for students on careers, skills and future planning.",
        "img": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    },
    {
        "title": "Blood Donation Camp",
        "desc": "Emergency blood donation support for people in need.",
        "img": "https://cdn-icons-png.flaticon.com/512/2913/2913465.png"
    },
    {
        "title": "Social Awareness Drive",
        "desc": "Programs on drugs, mobile addiction and social issues.",
        "img": "https://cdn-icons-png.flaticon.com/512/1046/1046784.png"
    },
    {
        "title": "Public Issues Program",
        "desc": "Collecting and forwarding public issues to authorities.",
        "img": "https://cdn-icons-png.flaticon.com/512/3063/3063822.png"
    }
]

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Yuva Shakti",
    page_icon="🧡",
    layout="mobile"
)

# ---------------- UTIL FUNCTIONS ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(phone, name, password):
    users = load_users()
    if phone in users:
        return False
    users[phone] = {
        "name": name,
        "password": hash_password(password),
        "joined_on": str(datetime.now())
    }
    save_users(users)
    return True

def login_user(phone, password):
    users = load_users()
    if phone in users and users[phone]["password"] == hash_password(password):
        return users[phone]["name"]
    return None

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stButton>button {
    width:100%;
    background:#FF6600;
    color:white;
    border-radius:10px;
}
.card {
    padding:10px;
    border-radius:12px;
    background:#fff5ee;
    margin-bottom:10px;
}
h2,h3 {
    text-align:center;
    color:#FF6600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🧡 Yuva Shakti 🇮🇳")

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["Login 🔐", "Register 📝"])

    with tab1:
        phone = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            name = login_user(phone, password)
            if name:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_phone = phone
                st.rerun()
            else:
                st.error("Invalid details")

    with tab2:
        st.info("ℹ️ OTP verification done in Android App (Firebase)")
        name = st.text_input("Full Name")
        phone = st.text_input("Mobile Number (OTP Verified)")
        password = st.text_input("Create Password", type="password")
        if st.button("Register"):
            if name and phone and password:
                if register_user(phone, name, password):
                    st.success("Registered successfully! Login now.")
                else:
                    st.error("User already exists")
            else:
                st.warning("Fill all fields")

# ---------------- DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    menu = st.sidebar.radio(
        "Menu",
        ["Home", "Programs", "Attendance", "Report Issue", "Emergency", "Profile"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # HOME
    if menu == "Home":
        st.info("📢 Sunday meeting at ZPHS School – Attendance compulsory")
        st.success("Welcome to Yuva Shakti 🇮🇳")

    # PROGRAMS GALLERY
    elif menu == "Programs":
        st.subheader("📸 Our Programs")
        for p in PROGRAMS:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(p["img"], width=80)
            st.write(f"**{p['title']}**")
            st.write(p["desc"])
            st.markdown("</div>", unsafe_allow_html=True)

    # ATTENDANCE
    elif menu == "Attendance":
        if st.button("✅ Mark Attendance"):
            today = datetime.now().strftime("%d-%m-%Y")
            msg = f"*Attendance*%0AName:{st.session_state.user_name}%0ADate:{today}"
            st.link_button("Confirm via WhatsApp", f"https://wa.me/{ADMIN_PHONE}?text={msg}")

    # REPORT ISSUE
    elif menu == "Report Issue":
        area = st.text_input("Area / Ward")
        issue = st.selectbox("Issue Type", ["Street Light", "Road", "Drainage", "Other"])
        desc = st.text_area("Description")
        if st.button("Send Complaint"):
            msg = f"*Complaint*%0AName:{st.session_state.user_name}%0AArea:{area}%0AIssue:{issue}%0ADetails:{desc}"
            st.link_button("Send via WhatsApp", f"https://wa.me/{ADMIN_PHONE}?text={msg}")

    # EMERGENCY CONTACTS
    elif menu == "Emergency":
        st.subheader("🚨 Emergency Contacts")
        for name, num in EMERGENCY_CONTACTS.items():
            st.link_button(f"📞 {name}", f"https://wa.me/{num}")

    # PROFILE
    elif menu == "Profile":
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Phone:** {st.session_state.user_phone}")
        st.success("Active Member")
