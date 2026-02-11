import streamlit as st
import requests

# URL adresa, ktorú dostaneš od Renderu (napr. https://mv-backend.onrender.com)
API = st.secrets["backend_url"] + "/posts"

st.set_page_config(page_title="Admin Panel", page_icon="⚫")
st.title("Admin Panel")

with st.form("new_post", clear_on_submit=True):
    t = st.text_input("Nadpis")
    m = st.text_area("Text statusu")
    if st.form_submit_button("Publikovať"):
        if t and m:
            res = requests.post(API, json={"title": t, "text": m})
            if res.status_code == 200: st.success("Status bol úspešne odoslaný!")
            else: st.error(f"Chyba: {res.status_code}")
        else: st.warning("Vyplň obidve polia.")

st.divider()
if st.button("Načítať feed pre kontrolu"):
    data = requests.get(API).json()
    for p in data:
        st.subheader(p['title'])
        st.write(p['text'])
        st.caption(p['at'])
        st.divider()
