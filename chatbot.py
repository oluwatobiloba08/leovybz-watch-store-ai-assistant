def process_sales_query(user_query, df_catalog, owner_name):
    query_clean = user_query.lower()
    
    # 1. Flagship Recommendations
    if "recommend" in query_clean or "suggest" in query_clean or "best" in query_clean:
        return "I highly recommend checking out our premium **Hublot Big Bang Gold Classic** for elite luxury, or the rugged **G-Shock Mudmaster** if you need extreme durability! Scroll down our vertical feed to view their designs."
        
    # 2. Budget Inquiries
    elif "cheap" in query_clean or "budget" in query_clean or "lowest" in query_clean:
        if not df_catalog.empty:
            budget_pick = df_catalog.sort_values(by="price", ascending=True).iloc[0]
            return f"Our most accessible timepiece is the **{budget_pick['name']}** priced at just **₦{budget_pick['price']:,}**! It looks incredibly clean in person."
        return "Please inspect the catalog feed cards on the left column to review current model pricing lists."
        
    # 3. Direct Brand Target Filters (Kept for quick specific searches)
    elif "gshock" in query_clean or "g-shock" in query_clean:
        return "We carry high-end G-Shock models like the *Mudmaster Tactical*, the octagonal *GA-2100 CasiOak*, and the *Frogman Diver Pro*. They are fully shockproof and water-resistant!"
        
    elif "valenzo" in query_clean:
        return "Valenzo timepieces offer executive class at incredible value. Check out our *Valenzo Heritage Chronograph* or the sleek *Valenzo Minimalist Silver Mesh* cards in our feed."
        
    elif "hublot" in query_clean or "luxury" in query_clean:
        return "For absolute high-end luxury, look at our Hublot collection. We have the *Big Bang Gold Classic*, *Classic Fusion Titanium*, and the skeletonized *Spirit of Big Bang*."
        
    # 4. Purchase Flow / Checkout Help
    elif "buy" in query_clean or "order" in query_clean or "contact" in query_clean:
        return "Ordering is fast! Scroll down to your preferred watch model in the vertical shop column and click **'Place Order'**. The app will immediately generate your custom WhatsApp checkout link."
        
    # 5. General Greetings
    elif "hello" in query_clean or "hi " in query_clean:
        return "Hello there! How can I assist you with your shopping choices today?"
        
    # 6. UNIVERSAL SAFE FALLBACK
    else:
        return "Ask me about wrist watch brands."
