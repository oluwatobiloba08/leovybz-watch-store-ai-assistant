import pandas as pd
import os

DB_FILE = "catalog.csv"
IMAGE_FOLDER = "saved_images"

def init_db():
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
        
    if not os.path.exists(DB_FILE):
        # 🔥 THE ABSOLUTE CLEAN RESET FIX:
        # We define only the header columns with zero active data rows. 
        # The code will now generate a completely empty catalog spreadsheet on first initialization.
        columns = ["name", "price", "category", "description", "image_path"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(DB_FILE, index=False)

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
