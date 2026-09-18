import streamlit as st
import pandas as pd
import urllib.parse
import os
from database import get_catalog
from chatbot import process_sales_query
from admin import render_admin_panel, init_owner_config

st.set_page_config(page_title="LEOVYBZ Store", page_icon="🦁", layout="wide")

# Theme styling layout structural script variables
st.markdown("""
    <style>
    .main-title { font-size:44px !important; font-weight: bold; color: #D4AF37; text-align: center; margin-bottom: 2px; font-family: 'Georgia', serif; }
    .sub-title { font-size:16px !important; text-align: center; margin-bottom: 30px; color: #A0A0A0; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

init_owner_config()

tab_store, tab_admin = st.tabs(["🛒 LEOVYBZ Customer Storefront", "⚙️ Owner Management Admin"])

with tab_store:
    st.markdown('<div class="main-title">🦁 LEOVYBZ WATCHES</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">CHRONOGRAPHS & LUXURY TIMEPIECES DIRECT OUTLET</div>', unsafe_allow_html=True)
    
    col_feed, col_chat = st.columns(, gap="large")
    
    # --- PART A: VERTICAL PRODUCT SCROLL FEED ---
    with col_feed:
        st.subheader("Explore Our Collection")
        catalog_df = get_catalog()
        
        if catalog_df.empty:
            st.info("No timepieces currently logged inside the database array.")
        else:
            for index, watch in catalog_df.iterrows():
                with st.container(border=True):
                    
                    # Core physical path validation rendering loop
                    img_path = str(watch['image_path'])
                    if os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning("⚠️ Image file loading from server local path...")
                    
                    st.markdown(f"## {watch['name']}")
                    st.markdown(f"**Price:** ₦{watch['price']:,} | **Category:** {watch['category']}")
                    st.write(watch['description'])
                    
                    if st.button("Place Order", key=f"order_btn_{index}", type="primary", use_container_width=True):
                        st.markdown("---")
                        st.info("📝 **Order via this WhatsApp link**")
                        
                        text_payload = f"Hello LEOVYBZ, I am on your storefront web app and I want to purchase the watch model: *{watch['name']}* (₦{watch['price']:,})."
                        encoded_payload = urllib.parse.quote(text_payload)
                        
                        base_link = st.session_state.wa_base_url if st.session_state.wa_base_url.endswith('/') else st.session_state.wa_base_url + '/'
                        whatsapp_href = f"{base_link}?phone={st.session_state.owner_phone}&text={encoded_payload}"
                        
                        st.markdown(f"### [➡️ Click Here to Open WhatsApp & Complete Order]({whatsapp_href})")
                        st.markdown("---")
                        
    # --- PART B: SINGLE-RESPONSE INSTANT ASSISTANT ---
    with col_chat:
        st.subheader("Interactive Assistant")
        
        if "last_user_msg" not in st.session_state:
            st.session_state.last_user_msg = ""
        if "last_bot_reply" not in st.session_state:
            st.session_state.last_bot_reply = "Welcome to LEOVYBZ. I can search our catalog for models, analyze budget items, or guide you through checkout. Ask me a question below!"

        if st.session_state.last_user_msg:
            with st.chat_message("user"):
                st.write(st.session_state.last_user_msg)
                
        with st.chat_message("assistant"):
            st.write(st.session_state.last_bot_reply)
                
        if user_msg := st.chat_input("Ask a question about our timepieces..."):
            st.session_state.last_user_msg = user_msg
            reply = process_sales_query(user_msg, catalog_df, st.session_state.owner_name)
            st.session_state.last_bot_reply = reply
            st.rerun()

with tab_admin:
    render_admin_panel()
