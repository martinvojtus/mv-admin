import streamlit as st
import requests

# --- CONFIG ---
st.set_page_config(page_title="Admin Panel", page_icon=None)

# --- 1. LOGIN (Directly on page) ---
# Check password immediately. If wrong, stop the app.
password = st.text_input("Password", type="password")

if password != st.secrets["admin_password"]:
    st.stop()  # Stop here if password is empty or wrong

# --- 2. ADMIN INTERFACE (Only visible if password is correct) ---
st.title("Admin Panel")

API = st.secrets["backend_url"] + "/posts"

# Form for new post
with st.form("new_post", clear_on_submit=True):
    title = st.text_input("Title")
    text = st.text_area("Content")
    
    # Submit button
    if st.form_submit_button("Publish"):
        if title and text:
            try:
                res = requests.post(API, json={"title": title, "text": text})
                if res.status_code == 200:
                    st.success("Post published successfully.")
                else:
                    st.error(f"Server error: {res.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please fill in both fields.")

st.divider()

# Feed preview
if st.button("Refresh Feed"):
    try:
        data = requests.get(API).json()
        if not data:
            st.info("No posts found.")
        
        for p in data:
            st.subheader(p['title'])
            st.text(p['at'])
            st.write(p['text'])
            st.divider()
    except:
        st.error("Failed to load data.")
