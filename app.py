import streamlit as st
import requests

# --- KONFIGURÁCIA ---
st.set_page_config(page_title="Admin Panel", page_icon="🔒")

# --- 1. PRIHLASOVANIE ---
# Vypýtame si heslo v bočnom paneli
heslo = st.sidebar.text_input("Zadaj heslo", type="password")

# Porovnáme ho s heslom v Secrets
if heslo == st.secrets["admin_password"]:
    
    # --- 2. AK JE HESLO SPRÁVNE, UKÁŽE SA ADMIN ---
    st.title("✅ Admin Panel")
    
    API = st.secrets["backend_url"] + "/posts"

    with st.form("new_post", clear_on_submit=True):
        t = st.text_input("Nadpis")
        m = st.text_area("Text statusu")
        
        if st.form_submit_button("Publikovať"):
            if t and m:
                try:
                    res = requests.post(API, json={"title": t, "text": m})
                    if res.status_code == 200:
                        st.success("Status bol úspešne odoslaný! 🚀")
                    else:
                        st.error(f"Chyba servera: {res.status_code}")
                except Exception as e:
                    st.error(f"Chyba spojenia: {e}")
            else:
                st.warning("Vyplň obidve polia.")

    st.divider()
    if st.button("Načítať feed pre kontrolu"):
        try:
            data = requests.get(API).json()
            for p in data:
                st.subheader(p['title'])
                st.write(p['text'])
                st.caption(f"ID: {p['id']} | {p['at']}")
                st.divider()
        except:
            st.error("Nepodarilo sa načítať dáta.")

else:
    # --- 3. AK JE HESLO ZLE (ALEBO ŽIADNE) ---
    st.warning("🔒 Pre vstup do Admin panela zadaj heslo vľavo.")
    st.stop()
