import streamlit as st
import pandas as pd
import urllib.parse
import os
from database import get_catalog
from chatbot import process_sales_query
from admin import render_admin_panel, init_owner_config

# 1. PAGE AND THEME STRUCTURE CONFIGS
st.set_page_config(page_title="LEOVYBZ Store", page_icon="🦁", layout="wide")

# 🔥 ADVANCED CUSTOM CSS INJECTION: LUXURY BLACK & GOLD THEME
st.markdown("""
    <style>
    /* Force the main background container to deep luxury charcoal black */
    .stApp {
        background-color: #0d0d0d !important;
        color: #f0f0f0 !important;
    }
    
    /* Global Typography Resets for dark contrast */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Branding Header Typography Styles */
    .main-title { 
        font-size: 48px !important; 
        font-weight: 900; 
        color: #D4AF37 !important; /* Pure Metallic Gold */
        text-align: center; 
        margin-bottom: 2px; 
        font-family: 'Georgia', serif;
        letter-spacing: 3px;
        text-shadow: 0px 4px 10px rgba(212, 175, 55, 0.2);
    }
    .sub-title { 
        font-size: 14px !important; 
        text-align: center; 
        margin-bottom: 35px; 
        color: #A3A3A3 !important; 
        letter-spacing: 4px; 
        font-weight: 500;
    }
    
    /* Restyle Streamlit Container Boxes with thin gold border accents */
    [data-testid="stContainer"] {
        background-color: #1a1a1a !important; /* Slightly lighter carbon black */
        border: 1px solid #D4AF37 !important; /* Gold perimeter line */
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 25px !important;
    }
    
    /* Restyle the "Place Order" Red/Blue button to solid Black & Gold */
    div.stButton > button {
        background-color: #D4AF37 !important; /* Metallic Gold Background */
        color: #000000 !important; /* Crisp black text inside */
        font-weight: bold !important;
        font-size: 16px !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #ffffff !important; /* Bright shift on mouse hover */
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        box-shadow: 0px 0px 12px rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Restyle the Chat Messenger Entry Text Bar Input box area */
    div[data-testid="stChatInput"] input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* Format the dynamic custom WhatsApp clickable hyperlinks layout */
    .whatsapp-link-box {
        background-color: #0a2412 !important; /* Forest green fallback context banner */
        border-left: 5px solid #25D366 !important; /* Classic WhatsApp branding stripe */
        padding: 15px !important;
        border-radius: 6px !important;
        margin-top: 15px !important;
    }
    .whatsapp-link-box a {
        color: #25D366 !important;
        font-weight: bold !important;
        text-decoration: none !important;
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

init_owner_config()

tab_store, tab_admin = st.tabs(["🛒 LEOVYBZ Customer Storefront", "⚙️ Owner Management Admin"])

# ========================================================
# TAB 1: CUSTOMER VIEW (VERTICAL STREAMED INTERFACE)
# ========================================================
with tab_store:
    st.markdown('<div class="main-title">🦁 LEOVYBZ WATCHES</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">CHRONOGRAPHS & LUXURY TIMEPIECES DIRECT OUTLET</div>', unsafe_allow_html=True)
    
    col_feed, col_chat = st.columns([3, 2], gap="large")
    
    # --- PART A: VERTICAL PRODUCT SCROLL FEED ---
    with col_feed:
        st.subheader("🏆 Explore Our Collection")
        catalog_df = get_catalog()
        
        if catalog_df.empty:
            st.info("No timepieces currently logged inside the database array.")
        else:
            for index, watch in catalog_df.iterrows():
                with st.container():
                    
                    # DYNAMIC IMAGE DETECTOR FIX:
                    # Renders external web placeholder references or physical uploaded assets smoothly
                    img_path = str(watch['image_path'])
                    if img_path.startswith("http"):
                        st.image(img_path, use_container_width=True)
                    elif os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning("⚠️ Image asset could not be located on database drive disk")
                    
                    st.markdown(f"## {watch['name']}")
                    st.markdown(f"**Price:** ₦{watch['price']:,} | **Category:** {watch['category']}")
                    st.write(watch['description'])
                    
                    if st.button("Place Order", key=f"order_btn_{index}", use_container_width=True):
                        st.markdown("---")
                        st.info("📝 **Order via this WhatsApp link**")
                        
                        text_payload = f"Hello LEOVYBZ, I am on your storefront web app and I want to purchase the watch model: *{watch['name']}* (₦{watch['price']:,})."
                        encoded_payload = urllib.parse.quote(text_payload)
                        
                        base_link = st.session_state.wa_base_url if st.session_state.wa_base_url.endswith('/') else st.session_state.wa_base_url + '/'
                        whatsapp_href = f"{base_link}?phone={st.session_state.owner_phone}&text={encoded_payload}"
                        
                        # Wrapped inside our custom styled notification link panel anchor structure block
                        st.markdown(f"""
                            <div class="whatsapp-link-box">
                                <a href="{whatsapp_href}" target="_blank">➡️ CLICK HERE TO OPEN WHATSAPP & COMPLETE ORDER</a>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown("---")
                        
    # --- PART B: SINGLE-RESPONSE INSTANT ASSISTANT ---
    with col_chat:
        st.subheader("💬 Interactive Assistant")
        
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
