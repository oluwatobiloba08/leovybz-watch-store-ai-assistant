import streamlit as st
import pandas as pd
import urllib.parse
import os
from database import get_catalog
from chatbot import process_sales_query
from admin import render_admin_panel, init_owner_config

# 1. PAGE AND THEME STRUCTURE CONFIGS
st.set_page_config(page_title="LEOVYBZ Store", page_icon="🦁", layout="wide")

# 🔥 CUSTOM CSS INJECTION: LUXURY BLACK & GOLD THEME
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
    
    /* Restyle the Chat Messenger Entry Text Bar Input box area */
    div[data-testid="stChatInput"] input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* Style the green markdown link text specifically for high-end look */
    .stMarkdown a {
        color: #25D366 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        text-decoration: underline !important;
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
    
    # Balanced structural split-screen layout proportions array
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
                    
                    # DYNAMIC IMAGE RENDERING MECHANIC:
                    img_path = str(watch['image_path'])
                    if img_path.startswith("http"):
                        st.image(img_path, use_container_width=True)
                    elif os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning(f"⚠️ Image file could not be located at {img_path}")
                    
                    st.markdown(f"## {watch['name']}")
                    st.markdown(f"**Price:** ₦{watch['price']:,} | **Category:** {watch['category']}")
                    st.write(watch['description'])
                    
                    # BULLETPROOF STATIC ROUTING STRUCTURE:
                    text_payload = f"Hello LEOVYBZ, I want to place an order for the product: *{watch['name']}* (₦{watch['price']:,}) from your web app!"
                    encoded_payload = urllib.parse.quote(text_payload)
                    whatsapp_href = f"https://wa.me{encoded_payload}"
                    
                    # Native framework markdown texts sitting cleanly on the card face.
                    # It displays your required note format and acts as a completely unblockable anchor.
                    st.caption("📝 **Order via this WhatsApp link**")
                    st.markdown(f"[➡️ CLICK HERE TO PLACE YOUR ORDER ON WHATSAPP]({whatsapp_href})")
                        
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
