import pandas as pd
import os

DB_FILE = "catalog.csv"
IMAGE_FOLDER = "saved_images"

def init_db():
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
        
    if not os.path.exists(DB_FILE):
        columns = ["name", "price", "category", "description", "image_path"]
        df = pd.DataFrame(columns=columns)
        df.to_csv(DB_FILE, index=False)

def get_catalog():
    init_db()
    df = pd.read_csv(DB_FILE)
    df = df.dropna(subset=['name'])
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

# Automatically trigger database and folder creation when imported/executed
init_db()
