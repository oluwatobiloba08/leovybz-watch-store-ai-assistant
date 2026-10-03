import pandas as pd
import os

# =========================================================================
# 💾 DATABASE UTILITY FUNCTIONS (DATABASE & DASHBOARD MANAGEMENT)
# =========================================================================

DB_FILE = "catalog.csv"
IMAGE_FOLDER = "saved_images"

def init_db():
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
        
    if not os.path.exists(DB_FILE):
        # Header setup with zero initial rows
        columns = ["name", "price", "category", "description", "image_path"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(DB_FILE, index=False)

def get_catalog():
    init_db()
    df = pd.read_csv(DB_FILE)
    # Clean out blank rows and format prices cleanly as integers
    df = df.dropna(subset=['name'])
    if not df.empty and 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int)
    return df

def add_product_to_db(name, price, category, description, image_source):
    df = get_catalog()
    new_row = pd.DataFrame([{
        "name": name,
        "price": int(price),
        "category": category,
        "description": description,
        "image_path": image_source
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def delete_product_from_db(product_name):
    df = get_catalog()
    # Removes deleted item dynamically from CSV
    df = df[df['name'].str.strip().str.lower() != product_name.strip().lower()]
    df.to_csv(DB_FILE, index=False)

def update_product_in_db(old_name, new_name, price, category, description, image_source):
    df = get_catalog()
    mask = df['name'].str.strip().str.lower() == old_name.strip().lower()
    
    if mask.any():
        df.loc[mask, 'name'] = new_name
        df.loc[mask, 'price'] = int(price)
        df.loc[mask, 'category'] = category
        df.loc[mask, 'description'] = description
        df.loc[mask, 'image_path'] = image_source
        df.to_csv(DB_FILE, index=False)

# Auto-initialize database on script creation/run
init_db()


# =========================================================================
# 🤖 CHATBOT SALES LOGIC (FULL 20-QUESTION TARGETED MATRIX)
# =========================================================================

def process_sales_query(user_query, df_catalog, owner_name):
    query_clean = user_query.lower().strip()
    
    # SAFETY CHECK: Fallback if the spreadsheet is completely blank
    if df_catalog.empty:
        return "Welcome to LEOVYBZ! Our digital showroom inventory is currently being updated by management. Please talk to our store owner or ask me again shortly!"

    # Clean catalog and ensure prices are numeric
    df_catalog = df_catalog.dropna(subset=['name']).copy()
    if 'price' in df_catalog.columns:
        df_catalog['price'] = pd.to_numeric(df_catalog['price'], errors='coerce').fillna(0).astype(int)

    # Extract all active watch names directly from live CSV
    active_items = df_catalog['name'].tolist()

    # Helper function to format watch names along with their exact prices
    def format_matches_with_price(matches_df):
        formatted_list = []
        for _, row in matches_df.iterrows():
            formatted_list.append(f"*{row['name']}* (₦{int(row['price']):,})")
        return ", ".join(formatted_list)

    # =========================================================================
    # 🎯 20-QUESTION TARGETED STOREFRONT MATRIX
    # =========================================================================

    # --- CATEGORY A: GENERAL CONVERSATION & BRANDING (Questions 1 - 5) ---
    
    # Q1: General Hello Greetings
    if any(greet in query_clean for greet in ["hello", "hi ", "hey ", "good day"]):
        return "Hello there! Welcome to LEOVYBZ Timepieces. I am your virtual sales manager. Ask me about our available watch brands, current budget entries, or flagship recommendations!"
    
    # Q2: Store Name Identification
    elif "your name" in query_clean or "who are you" in query_clean or "store name" in query_clean:
        return "You are currently shopping at **LEOVYBZ**, Nigeria's premium direct outlet for luxury, chronological, and tactical wristwatches."
    
    # Q3: Available Watch Brands List
    elif "brand" in query_clean or "brands" in query_clean or "what do you have" in query_clean:
        if df_catalog.empty:
            return "Our inventory feed is currently empty. Check back in a moment as management adds new items!"
        
        unique_brands = set([str(name).split()[0] for name in active_items if str(name).strip()])
        brands_string = ", ".join(sorted(unique_brands))
        return f"We proudly showcase the following premium watch brands right now: **{brands_string}**. You can scroll down our main vertical feed to check out their specific models and configurations!"
    
    # Q4: Business Location / Shop Address
    elif "location" in query_clean or "where is your shop" in query_clean or "where are you based" in query_clean or "office" in query_clean or "address" in query_clean:
        return "The LEOVYBZ main head office is located at **Ikorodu, Igbe Road**. While our physical management desk is situated here, we operate primarily as a premium digital storefront delivering timepieces nationwide directly to your doorstep."
    
    # Q5: Hours of Operation
    elif "time" in query_clean or "open" in query_clean or "close" in query_clean or "working hours" in query_clean:
        return "Our digital storefront is open for browsing 24/7! Our order processing desk and WhatsApp chat support lines are highly active daily from 8:00 AM to 10:00 PM."


    # --- CATEGORY B: THE 3 CORE BRAND FILTERS (Questions 6 - 11) ---
    
    # Q6 & Q7: G-Shock Inquiries (Brand & Specs + Price)
    elif "gshock" in query_clean or "g-shock" in query_clean or "rugged watch" in query_clean or "shockproof" in query_clean:
        gshock_df = df_catalog[df_catalog['name'].str.lower().str.contains("g-shock|gshock", na=False)]
        if not gshock_df.empty:
            matches_str = format_matches_with_price(gshock_df)
            return f"Yes! We carry rugged G-Shock models right now: {matches_str}. They feature carbon core guards, complete shock resistance, and heavy-duty waterproofing."
        return "We currently don't have any G-Shock models left in our active stock collection. Let me know if you would like to explore our other executive watch brands!"

    # Q8 & Q9: Valenzo Inquiries (Brand & Specs + Price)
    elif "valenzo" in query_clean or "mesh band" in query_clean or "leather strap" in query_clean or "minimalist" in query_clean:
        valenzo_df = df_catalog[df_catalog['name'].str.lower().str.contains("valenzo", na=False)]
        if not valenzo_df.empty:
            matches_str = format_matches_with_price(valenzo_df)
            return f"Valenzo timepieces offer sharp executive elegance at incredible value. We currently showcase: {matches_str}. Check out their premium design spec cards in our vertical feed!"
        return "We currently don't have any Valenzo models available in our warehouse inventory. Let me know if you would like to explore our other luxury watch brands!"

    # Q10 & Q11: Hublot Inquiries (Brand & Specs + Price)
    elif "hublot" in query_clean or "luxury" in query_clean or "gold watch" in query_clean or "skeleton dial" in query_clean:
        hublot_df = df_catalog[df_catalog['name'].str.lower().str.contains("hublot", na=False)]
        if not hublot_df.empty:
            matches_str = format_matches_with_price(hublot_df)
            return f"For absolute high-end luxury and presidential class, explore our Hublot pieces. Our current active showroom features: {matches_str}. They look spectacular in person."
        return "We currently don't have any Hublot models left in our active stock. Let me know if you would like to explore our other premium watch brands!"


    # --- CATEGORY C: INVENTORY METRICS & ANALYSIS (Questions 12 - 15) ---
    
    # Q12: Flagship/Best Recommendations
    elif "recommend" in query_clean or "suggest" in query_clean or "best" in query_clean:
        premium_watch = df_catalog.sort_values(by="price", ascending=False).iloc[0]
        return f"I highly recommend checking out our current flagship timepiece: **{premium_watch['name']}** priced at **₦{int(premium_watch['price']):,}**. It represents elite luxury! You can find it right now in our vertical scroll feed."
        
    # Q13: Budget / Cheapest watch inquiries
    elif "cheap" in query_clean or "budget" in query_clean or "lowest" in query_clean:
        budget_watch = df_catalog.sort_values(by="price", ascending=True).iloc[0]
        return f"Our most accessible timepiece currently in stock is the **{budget_watch['name']}**, priced at just **₦{int(budget_watch['price']):,}**! It looks incredibly sleek and clean in person."
        
    # Q14: Pricing checks general query
    elif "price" in query_clean or "how much" in query_clean or "cost" in query_clean:
        return "All our prices are clearly marked in local **Nigerian Naira (₦)** right underneath each product image inside the vertical scrolling storefront feed on your left."

    # Q15: Stock availability check general query
    elif "available" in query_clean or "in stock" in query_clean or "inventory" in query_clean:
        return f"Our digital inventory feed currently displays {len(df_catalog)} verified, active watch configurations. Everything you see on screen right now is fully available for delivery."


    # --- CATEGORY D: PURCHASE LOGISTICS & CUSTOMER SERVICE (Questions 16 - 20) ---
    
    # Q16: How to place an order
    elif "buy" in query_clean or "order" in query_clean or "checkout" in query_clean:
        return "Ordering is incredibly seamless! Simply scroll down to your preferred watch model in the vertical shop column and click the gold **'Place Order'** button. The app will immediately copy our WhatsApp number directly to your clipboard so we can wrap up your checkout in our DM."
        
    # Q17: Direct Phone Contact Info
    elif "phone" in query_clean or "number" in query_clean or "whatsapp" in query_clean:
        return "Our official business WhatsApp hotline line is **07076967421**. You can tap 'Place Order' on any product card to automatically copy it straight to your clipboard!"
    
    # Q18: Delivery Fees & Locations
    elif "delivery" in query_clean or "ship" in query_clean or "courier" in query_clean:
        return "We offer premium courier delivery services across all states in Nigeria. Delivery time is 24-48 hours within Lagos and 3-5 working days for interstate regional shipments."
        
    # Q19: Payment Methods & Cash on Delivery (COD)
    elif "pay" in query_clean or "bank transfer" in query_clean or "cash on delivery" in query_clean or "cod" in query_clean:
        return "We accept secure Bank Transfers and verified online payments. Cash on Delivery (COD) parameters can be finalized inside our private WhatsApp chat depending on your delivery address coordinates."

    # Q20: Product Authenticity / Original Guarantee
    elif "original" in query_clean or "authentic" in query_clean or "warranty" in query_clean or "fake" in query_clean:
        return "Every watch catalog item distributed through LEOVYBZ is 100% authentic, brand new, and comes backed by our official store warranty verification card."


    # =========================================================================
    # ❌ UNIVERSAL OFF-TOPIC FIREWALL CATCH ALL
    # =========================================================================
    else:
        return "Ask me about wrist watch."
