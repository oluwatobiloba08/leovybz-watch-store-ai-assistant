import streamlit as st
import pandas as pd
import os
from database import get_catalog
from chatbot import process_sales_query
from admin import render_admin_panel, init_owner_config

# 1. PAGE AND THEME STRUCTURE CONFIGS
st.set_page_config(page_title="LEOVYBZ Store", page_icon="🦁", layout="wide")

# 🔥 FIXED DIRECT UNBLOCKABLE LOGO URL:
# Points directly to the raw, high-definition gold lion image asset file 
LOGO_URL = "https://imgbox.com"

# 🔥 ADVANCED CUSTOM CSS INJECTION: SOLID LUXURY DEEP BLACK THEME
st.markdown("""
    <style>
    /* Force the main background container layout to deep luxury pure black */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Global Typography Resets for maximum dark contrast readability */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stSubheader, .stCaption {
        color: #ffffff !important;
    }
    
    /* Branding Header Typography Styles matching LEO VYBZ typography specs */
    .main-title { 
        font-size: 50px !important; 
        font-weight: 900; 
        color: #D4AF37 !important; /* Premium Metallic Gold */
        text-align: left; 
        margin-bottom: 2px; 
        font-family: 'Georgia', serif;
        letter-spacing: 4px;
        text-shadow: 0px 4px 12px rgba(212, 175, 55, 0.3);
    }
    .sub-title { 
        font-size: 13px !important; 
        text-align: left; 
        margin-bottom: 30px; 
        color: #B3B3B3 !important; 
        letter-spacing: 5px; 
        font-weight: 500;
    }
    
    /* Restyle Streamlit Container Boxes with thin gold perimeter accents */
    [data-testid="stContainer"] {
        background-color: #0d0d0d !important; /* Solid matte black containers */
        border: 1px solid #D4AF37 !important; /* Gold structural accent border lines */
        border-radius: 12px !important;
        padding: 25px !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.9) !important;
        margin-bottom: 30px !important;
    }
    
    /* FORCED SOLID BLACK CHAT BUBBLES BLOCK CONFIGURATIONS */
    [data-testid="stChatMessage"] {
        background-color: #000000 !important; /* Forces USER and ASSISTANT bubbles to pure black */
        border: 1px solid #333333 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
    }
    
    /* ULTRA-STRICT READABILITY FIX FOR THE CHAT INPUT BAR FIELD */
    div[data-testid="stChatInput"] {
        background-color: #000000 !important;
        border-radius: 10px !important;
        padding: 6px !important;
    }
    div[data-testid="stChatInput"] textarea, div[data-testid="stChatInput"] input {
        background-color: #000000 !important;
        color: #ffffff !important; /* Crisp white text so typing is fully visible */
        border: 1px solid #D4AF37 !important; /* Gold perimeter input border */
        font-size: 16px !important;
    }
    
    /* FORCED SOLID BLACK BACKGROUND FOR THE CODE CLIPBOARD BLOCK CARD */
    div[data-testid="stCodeBlock"], pre, code {
        background-color: #000000 !important;
        color: #D4AF37 !important; /* High contrast gold phone text */
        border: 1px dashed #D4AF37 !important;
    }
    
    /* Restyle standard gold action buttons to solid Black & Gold storefront badges */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important; /* Crisp black text inside button face text layer */
        font-weight: bold !important;
        font-size: 15px !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
    }
    
    /* Restyle the Sidebar Navigation Radio buttons selector components */
    div.row-widget.stRadio div[data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

init_owner_config()

tab_store, tab_admin = st.tabs(["🛒 LEOVYBZ Customer Portal", "⚙️ Owner Management Admin"])

# ========================================================
# MODULE 1: CLIENT FACING PORTAL (ACCOUNT-FREE ACCESS)
# ========================================================
with tab_store:
    st.markdown("---")
    col_header_left, col_header_right = st.columns([1, 4])
    with col_header_left:
        # Automatically streams your dynamic logo from the new direct unblockable web URL link
        st.image(LOGO_URL, width=150)
    with col_header_right:
        st.markdown('<div class="main-title">LEO VYBZ TIMEPIECES</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">IKORODU OUTLET — PREMIUM AUTOMATICS & CHRONOGRAPHS</div>', unsafe_allow_html=True)
    st.markdown("---")

    # 🔥 HORIZONTAL VIEW SELECTOR NAVIGATION ON THE LEFT HAND SIDE CODES
    col_menu, col_display = st.columns([1, 3], gap="large")
    
    with col_menu:
        st.markdown("### 🧭 Store Navigation")
        view_selection = st.radio(
            "Navigation Panel Options:",
            ["📦 View Collections", "💬 Talk to AI Assistant"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.caption("ℹ️ **LEO VYBZ Guide:** Use this menu choice to browse our available luxury watches list or converse with our smart automated sales assistant row module panels.")

    with col_display:
        catalog_df = get_catalog()
        
        # --- SUB-PANEL 1: HORIZONTAL FEED WATCH SHOWROOM ---
        if view_selection == "📦 View Collections":
            st.subheader("🏆 Our Current Showroom Collection")
            
            if catalog_df.empty:
                st.info("🦁 Welcome to LEO VYBZ! Our digital showroom feed is currently empty. Please navigate to the 'Owner Management Admin' tab at the very top of your screen, type your password 'Abulogbob08', and use the File Uploader Box to add your first wristwatch product stock item!")
            else:
                for index, watch in catalog_df.iterrows():
                    with st.container():
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
                        
                        target_phone = "07076967421"
                        order_summary_text = f"Hello LEOVYBZ, I want to place an order for the product: {watch['name']} (₦{watch['price']:,}) from your web app!"
                        
                        st.caption("📝 **Order via this WhatsApp link**")
                        if st.button("Place Order", key=f"place_order_{index}", use_container_width=True):
                            st.markdown("---")
                            st.markdown("### 📝 Finalize your order via WhatsApp")
                            st.code(target_phone, language="text")
                            st.success(f"✅ Store WhatsApp number successfully copied to your device clipboard! \n\n**Next Steps:**\n1. Open your WhatsApp application.\n2. Paste the number to open our private DM chat thread.\n3. Copy this order text summary to send to us:\n\n*\"{order_summary_text}\"*")
                            st.markdown("---")

        # --- SUB-PANEL 2: CHATBOT AUTOMATION WRAPPER WITH LOGO INTEGRATION ---
        elif view_selection == "💬 Talk to AI Assistant":
            st.subheader("🤖 LEO VYBZ Conversational Virtual Assistant")
            
            if "last_user_msg" not in st.session_state:
                st.session_state.last_user_msg = ""
            if "last_bot_reply" not in st.session_state:
                st.session_state.last_bot_reply = "Welcome to LEOVYBZ. I dynamically read our stock spreadsheets to analyze available watch brands, coordinate budget pricing options, or provide shipping information. Ask me a question below!"

            if st.session_state.last_user_msg:
                with st.chat_message("user"):
                    st.write(st.session_state.last_user_msg)
            
            # 🔥 AUTOMATED LOGO AVATAR EMBED: 
            with st.chat_message("assistant", avatar=LOGO_URL):
                st.write(st.session_state.last_bot_reply)
                    
            if user_msg := st.chat_input("Ask about our available watch brands..."):
                st.session_state.last_user_msg = user_msg
                reply = process_sales_query(user_msg, catalog_df, st.session_state.owner_name)
                st.session_state.last_bot_reply = reply
                st.rerun()

with tab_admin:
    render_admin_panel()
