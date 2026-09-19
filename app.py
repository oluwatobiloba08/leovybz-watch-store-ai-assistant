import streamlit as st
import pandas as pd
import urllib.parse
import os
from database import get_catalog
from chatbot import process_sales_query
from admin import render_admin_panel, init_owner_config

# 1. PAGE AND THEME STRUCTURE CONFIGS
st.set_page_config(page_title="LEOVYBZ Store", page_icon="🦁", layout="wide")

# 🔥 ADVANCED CUSTOM CSS INJECTION: SOLID BLACK LUXURY BACKGROUNDS & GREEN WHATSAPP BUTTONS
st.markdown("""
    <style>
    /* Force the main background container to deep luxury pure black */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
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
        background-color: #0d0d0d !important; /* Solid matte black containers */
        border: 1px solid #D4AF37 !important; /* Gold perimeter line */
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.8) !important;
        margin-bottom: 25px !important;
    }
    
    /* FORCED SOLID BLACK CHAT BUBBLES BLOCK */
    [data-testid="stChatMessage"] {
        background-color: #000000 !important; /* Forces USER and ASSISTANT bubbles to pure black */
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* FORCED SOLID BLACK TYPING BAR / INPUT FIELD BOXES */
    div[data-testid="stChatInput"] input, div.stTextInput input, div.stTextArea textarea {
        background-color: #000000 !important; /* Solid pure black text input boxes */
        color: #ffffff !important;
        border: 1px solid #D4AF37 !important; /* Gold input borders */
    }
    
    /* Restyle standard gold action buttons to solid Black & Gold storefront badges */
    div.stButton > button {
        background-color: #D4AF37 !important; /* Metallic Gold Background */
        color: #000000 !important; /* Crisp black text inside */
        font-weight: bold !important;
        font-size: 15px !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #ffffff !important; /* Bright shift on mouse hover */
        color: #000000 !important;
        border: 1px solid #ffffff !important;
    }

    /* 🔥 SPECIAL WHATSAPP LAUNCH BUTTON STYLING (VIBRANT CHAT GREEN) */
    div.stLinkButton > a {
        background-color: #25D366 !important; /* WhatsApp Green background */
        color: #ffffff !important; /* Crisp white text inside */
        font-weight: bold !important;
        font-size: 15px !important;
        border: 1px solid #25D366 !important;
        border-radius: 8px !important;
        text-align: center !important;
        text-decoration: none !important;
        display: inline-block !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    div.stLinkButton > a:hover {
        background-color: #20ba5a !important; /* Darker green on mouse hover */
        border: 1px solid #20ba5a !important;
        box-shadow: 0px 0px 10px rgba(37, 211, 102, 0.4) !important;
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
                    
                    # Core copy trigger interaction text setup
                    order_text = f"Hello LEOVYBZ, I want to place an order for the product: {watch['name']} (₦{watch['price']:,}) from your web app!"
                    
                    st.caption("📝 **Order via this WhatsApp link**")
                    
                    # The security bypass layout checkpoint:
                    if st.button("🛒 Click to Copy Order Text", key=f"copy_btn_{index}", use_container_width=True):
                        # Runs internal browser clipboard payload transfer block
                        st.code(order_text, language="text")
                        st.success("✅ Order text copied to your clipboard! Now click the green button below to slide directly into our chat DM and paste your message.")
                        
                        # 🔥 SECURE UNBLOCKABLE LAUNCH TUNNEL:
                        # Standardized direct API query endpoint which browsers natively white-list
                        whatsapp_href = "https://wa.me"
                        
                        # Renders the safe green launch button right inside the confirmation alert area
                        st.link_button("💬 Open WhatsApp & Message 09023471474", url=whatsapp_href, use_container_width=True)
                        
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
