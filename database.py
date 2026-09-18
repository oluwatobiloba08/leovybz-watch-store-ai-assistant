import pandas as pd
import os
import urllib.request

DB_FILE = "catalog.csv"
IMAGE_FOLDER = "saved_images"

def download_starter_images():
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
        
    # High-quality fallback images to bypass hotlink blocks
    img_urls = {
        "watch_1.jpg": "https://unsplash.com",
        "watch_2.jpg": "https://unsplash.com",
        "watch_3.jpg": "https://unsplash.com",
        "watch_4.jpg": "https://unsplash.com",
        "watch_5.jpg": "https://unsplash.com",
        "watch_6.jpg": "https://unsplash.com",
        "watch_7.jpg": "https://unsplash.com",
        "watch_8.jpg": "https://unsplash.com",
        "watch_9.jpg": "https://unsplash.com",
        "watch_10.jpg": "https://unsplash.com"
    }
    
    for filename, url in img_urls.items():
        local_path = os.path.join(IMAGE_FOLDER, filename)
        if not os.path.exists(local_path):
            try:
                # Force local stream caching download
                urllib.request.urlretrieve(url, local_path)
            except Exception:
                pass

def init_db():
    download_starter_images()
        
    if not os.path.exists(DB_FILE):
        default_watches = pd.DataFrame([
            {"name": "G-Shock Mudmaster Tactical", "price": 280000, "category": "Sports", "description": "Ultra-rugged, shockproof structure, mud-resistant casing, twin sensor compass.", "image_path": "saved_images/watch_1.jpg"},
            {"name": "Hublot Big Bang Gold Classic", "price": 4500000, "category": "Luxury", "description": "18k King Gold satin finish casing, exposed skeleton dial, structural rubber strap.", "image_path": "saved_images/watch_2.jpg"},
            {"name": "Valenzo Heritage Chronograph", "price": 185000, "category": "Chronograph", "description": "Premium leather dress strap, champagne gold accent finish, Japanese quartz precision.", "image_path": "saved_images/watch_3.jpg"},
            {"name": "G-Shock GA-2100 'CasiOak'", "price": 145000, "category": "Sports", "description": "Carbon core guard structure, octagonal bezel design, matte black finish profile.", "image_path": "saved_images/watch_4.jpg"},
            {"name": "Valenzo Minimalist Silver Mesh", "price": 120000, "category": "Minimalist", "description": "Surgical grade stainless steel mesh band, ultra-thin case, deep navy sunray dial face.", "image_path": "saved_images/watch_5.jpg"},
            {"name": "Hublot Classic Fusion Titanium", "price": 3800000, "category": "Luxury", "description": "Satin-finished titanium chassis, minimalist black dial face, premium deployment clasp.", "image_path": "saved_images/watch_6.jpg"},
            {"name": "G-Shock Frogman Diver Pro", "price": 395000, "category": "Sports", "description": "ISO 200m diver level water resistance, dive log tracking memory, solar powered movement.", "image_path": "saved_images/watch_7.jpg"},
            {"name": "Valenzo Executive Rose Gold", "price": 210000, "category": "Luxury", "description": "Polished rose gold plating, genuine alligator texture leather strap, automatic sweeping hand mechanics.", "image_path": "saved_images/watch_8.jpg"},
            {"name": "Hublot Spirit of Big Bang", "price": 5200000, "category": "Luxury", "description": "Tonneau-shaped carbon fiber matrix bezel, intricate open-worked chronological movement gears.", "image_path": "saved_images/watch_9.jpg"},
            {"name": "Valenzo Aviator Stealth Black", "price": 165000, "category": "Chronograph", "description": "High-contrast pilot dial accents, dual-time zone function tracking features, matte black structural coating.", "image_path": "saved_images/watch_10.jpg"}
        ])
        default_watches.to_csv(DB_FILE, index=False)

def get_catalog():
    init_db()
    return pd.read_csv(DB_FILE)

def add_product_to_db(name, price, category, description, image_source):
    df = pd.read_csv(DB_FILE)
    new_row = pd.DataFrame([{
        "name": name,
        "price": int(price),
        "category": category,
        "description": description,
        "image_path": image_source
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
