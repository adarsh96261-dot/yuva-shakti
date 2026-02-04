import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ---------------- CONFIG ----------------
DATA_FILE = "users_db.json"

st.set_page_config(
    page_title="Yuva Shakti",
    page_icon="🧡",
    layout="centered"
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

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stButton>button {
    width:100%;
    background:#FF6600;
    color:white;
    border-radius:10px;
}
h2 {
    text-align:center;
    color:#FF6600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🧡 Yuva Shakti")

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["Login 🔐", "Register 📝"])

    # LOGIN
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
                st.error("Invalid mobile number or password")

    # REGISTER (OTP verified users only)
    with tab2:
        st.info("ℹ️ OTP verification is done in Android App (Firebase)")
        name = st.text_input("Full Name")
        phone = st.text_input("Mobile Number (OTP Verified)")
        password = st.text_input("Create Password", type="password")

        if st.button("Register"):
            if name and phone and password:
                if register_user(phone, name, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("User already exists")
            else:
                st.warning("Please fill all fields")

# ---------------- DASHBOARD ----------------
else:
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    menu = st.sidebar.radio("Menu", ["Home", "Profile"])

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    if menu == "Home":
        st.success("Welcome to Yuva Shakti 🇮🇳")
        st.write("✔ Secure login")
        st.write("✔ OTP verified users")
        st.write("✔ Ready for Android APK")

    if menu == "Profile":
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Phone:** {st.session_state.user_phone}")
        st.success("Active Member")
