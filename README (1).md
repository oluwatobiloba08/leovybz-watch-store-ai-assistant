# 🦁 LEOVYBZ WATCH STORE — AI SALES ASSISTANT

Welcome to the official repository homepage for **LEOVYBZ**, a cloud-ready, interactive web storefront specializing in premium wristwatches (G-Shock, Valenzo, Hublot). This project combines a **Visual, Vertical-Scrolling E-Commerce Storefront** with an offline **Intelligent AI Sales Assistant** on a single screen layout.

---

## 🎨 Layout & Key Features

*   **No Customer Registration Required:** Customers get instant, friction-free access to browse the storefront immediately without having to create a profile account.
*   **Vertical Product Feed (Left 60%):** Designed to mimic a modern mobile shop interface (like Instagram Shop), allowing users to seamlessly scroll down through 10 pre-loaded luxury watch models.
*   **Interactive AI Sidebar (Right 40%):** A persistent chat messenger where users can ask for budget options or model recommendations at any point during their scroll.
*   **Instant WhatsApp Checkout:** Clicking the **"Place Order"** button under any watch card instantly reveals a custom, web-encoded WhatsApp link pre-filled with the exact watch details and local **Nigerian Naira (₦)** pricing.
*   **Secure Business Administration Panel:** A password-protected tab (`Abulogbob08`) built specifically for the store owner to change contact configuration settings and dynamically upload new watches using a local file uploader box.

---

## 🧱 Modular Architecture Blueprint

The project codebase is completely modularized following clean software engineering principles (**Separation of Concerns**), dividing features into distinct functional layers:

```text
📁 LEOVYBZ_STORE/
│
├── 📁 saved_images/        # Storage directory for newly uploaded local wristwatch photos
├── 📄 catalog.csv          # Relational text database storing watch names, prices, and file paths
├── 📄 requirements.txt     # Dependency environment tracking file
├── 📄 README.md            # Project technical documentation (This file)
│
├── 🐍 app.py               # Front-End user interface layout, theme styling, and view tabs
├── 🐍 database.py          # Data Access Layer (DAL) handling dataframe read/write loops
├── 🐍 chatbot.py           # Offline rule-based NLP text processing and matching engine
└── 🐍 admin.py             # Administrative access validation gate and product creation forms
```

---

## ⚙️ Detailed File Breakdown

### 1. `requirements.txt`
Specifies the environment package map. It guarantees a synchronized build process across deployment platforms.
```text
streamlit
pandas
```

### 2. `database.py` (Data Access Layer)
Protects runtime memory state. It automatically boots up the store on day one by writing 10 default watch items to disk, and tracks inventory using a local spreadsheet file (`catalog.csv`). **This ensures the app operates 100% free of charge with zero external cloud database dependencies.**

### 3. `chatbot.py` (Rule-Based AI Engine)
An intelligent, local conversational processor. By evaluating normalized text strings against specific keyword rules (e.g., `'cheap'`, `'recommend'`, `'gshock'`, `'hublot'`), it mimics a smart customer sales agent. If a customer types an off-topic question, it runs a fallback catch filter: *"Ask me about wrist watch brands."*

### 4. `admin.py` (Management Controller)
Houses administrative configuration tools. It protects business settings via strict string verification against the admin password. It incorporates a **Local File Uploader Box** that reads raw image binary streams from your computer or phone disk via `.getbuffer()`, duplicates them into the local directory, and appends the path pointer directly into the active database.

### 5. `app.py` (UI Orchestrator Front-End)
Sets up the presentation view grid. It uses pandas data loops (`.iterrows()`) to render visual product containers on the left column dynamically as the customer scrolls down. When "Place Order" is clicked, it calls `urllib.parse.quote()` to securely encode watch titles and Naira indices into a live click-to-chat hyperlink targeting the owner's WhatsApp number.

---


```
