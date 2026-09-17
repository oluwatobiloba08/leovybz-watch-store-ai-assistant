import streamlit as st
import pandas as pd
import os
from database import add_product_to_db

def init_owner_config():
    if "owner_phone" not in st.session_state:
        st.session_state.owner_phone = "07076967421"
    if "owner_name" not in st.session_state:
        st.session_state.owner_name = "LEOVYBZ Management"
    if "wa_base_url" not in st.session_state:
        st.session_state.wa_base_url = "https://whatsapp.com/dl/"

def render_admin_panel():
    init_owner_config()
    st.title("⚙️ Business Owner Management Panel")
    
    admin_password = st.text_input("Enter Dashboard Verification Password", type="password")
    
    if admin_password == "Abulogbob08":
        st.success("🔒 Access Granted. System configuration parameters unlocked.")
        
        st.subheader("📝 Edit User Contact Information")
        new_phone = st.text_input("WhatsApp Order Phone Number", value=st.session_state.owner_phone)
        new_url = st.text_input("WhatsApp Deep Link URL", value=st.session_state.wa_base_url)
        
        if st.button("Save Business Updates"):
            st.session_state.owner_phone = new_phone
            st.session_state.wa_base_url = new_url
            st.success("✅ Business details updated successfully!")
            
        st.subheader("➕ Add New Watch Model to Inventory")
        with st.form("add_watch_form", clear_on_submit=True):
            watch_name = st.text_input("Watch Name / Title")
            watch_price = st.number_input("Selling Price ($)", min_value=1, value=150)
            watch_cat = st.selectbox("Category Group", ["Luxury", "Chronograph", "Sports", "Minimalist"])
            watch_desc = st.text_area("Product Specifications")
            uploaded_file = st.file_uploader("Upload Product Image from Your Local File", type=["png", "jpg", "jpeg"])
            
            submit_btn = st.form_submit_button("Add Product")
            
            if submit_btn:
                if watch_name and watch_desc and uploaded_file is not None:
                    save_path = os.path.join("saved_images", f"{watch_name.replace(' ', '_')}_{uploaded_file.name}")
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        
                    add_product_to_db(watch_name, watch_price, watch_cat, watch_desc, save_path)
                    st.success(f"🎉 Success! '{watch_name}' added to inventory system directory layout!")
                    st.rerun()
                else:
                    st.error("⚠️ Incomplete form! You must complete all fields and select a file to upload.")
    elif admin_password != "":
        st.error("❌ Access Denied. Administrative credentials mismatch.")
