import streamlit as st
import requests

st.set_page_config(page_title="CMS Admin", layout="centered")

# --- LOGIN ---
password = st.text_input("Password", type="password")
if password != st.secrets["admin_password"]:
    st.stop()

# --- HLAVNÁ ČASŤ ---
st.title("Admin Dashboard")
BASE_URL = st.secrets["backend_url"]

# Session state pre uloženie ID statusu, ktorý práve editujeme
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# --- A. PRIDANIE / ÚPRAVA STATUSU ---
st.subheader("📝 Editor")

# Ak editujeme, predvyplníme formulár
edit_data = {}
if st.session_state.edit_id:
    st.info(f"Editing post ID: {st.session_state.edit_id}")
    # Nájdeme dáta k tomu statusu (z cache alebo reload)
    try:
        current_posts = requests.get(f"{BASE_URL}/posts").json()
        post_to_edit = next((p for p in current_posts if p['id'] == st.session_state.edit_id), None)
        if post_to_edit:
            edit_data = post_to_edit
    except:
        st.error("Error loading post data")

with st.form("post_form", clear_on_submit=True):
    # Ak máme dáta na editáciu, použijeme ich ako 'value', inak prázdne
    title_val = edit_data.get('title', "")
    text_val = edit_data.get('text', "")
    
    title = st.text_input("Title", value=title_val)
    text = st.text_area("Content", value=text_val, height=150)
    
    submitted = st.form_submit_button("Save / Publish")
    
    if submitted and title and text:
        try:
            if st.session_state.edit_id:
                # UPDATE (PUT)
                res = requests.put(f"{BASE_URL}/posts/{st.session_state.edit_id}", json={"title": title, "text": text})
                if res.status_code == 200:
                    st.success("Updated successfully!")
                    st.session_state.edit_id = None # Vypneme edit mód
                    st.rerun()
            else:
                # CREATE (POST)
                res = requests.post(f"{BASE_URL}/posts", json={"title": title, "text": text})
                if res.status_code == 200:
                    st.success("Published successfully!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Tlačidlo na zrušenie editácie
if st.session_state.edit_id:
    if st.button("Cancel Edit"):
        st.session_state.edit_id = None
        st.rerun()

st.divider()

# --- B. ZOZNAM STATUSOV (MANAGE) ---
st.subheader("📂 Manage Posts")

try:
    posts = requests.get(f"{BASE_URL}/posts").json()
    
    if not posts:
        st.info("No posts found.")
    
    for p in posts:
        # Vytvoríme 3 stĺpce: Text | Edit | Delete
        c1, c2, c3 = st.columns([6, 1, 1])
        
        with c1:
            st.markdown(f"**{p['title']}**")
            st.caption(f"{p['at'][:10]} | ID: {p['id']}")
        
        with c2:
            if st.button("✏️", key=f"edit_{p['id']}"):
                st.session_state.edit_id = p['id']
                st.rerun()
        
        with c3:
            if st.button("🗑️", key=f"del_{p['id']}"):
                requests.delete(f"{BASE_URL}/posts/{p['id']}")
                st.success("Deleted!")
                st.rerun()
        
        st.markdown("---")

except Exception as e:
    st.error(f"Failed to load feed: {e}")
