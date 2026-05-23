from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def create_welcome_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📦 Products", callback_data="menu_products")
    btn2 = InlineKeyboardButton("🛒 Cart", callback_data="menu_cart")
    btn3 = InlineKeyboardButton("📋 Orders", callback_data="menu_orders")
    btn4 = InlineKeyboardButton("👤 Profile", callback_data="menu_profile")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def create_product_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📦 Products", callback_data="menu_products")
    btn2 = InlineKeyboardButton("🛒 Cart", callback_data="menu_cart")
    btn3 = InlineKeyboardButton("📋 Orders", callback_data="menu_orders")
    btn4 = InlineKeyboardButton("👤 Profile", callback_data="menu_profile")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def create_product_buttons(products):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        btn = InlineKeyboardButton(
            f"{product.name} - ${product.price}", callback_data=f"product_{product.id}"
        )
        keyboard.add(btn)
    return keyboard


def create_product_detail_buttons(product_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(
        "➕ Add to Cart", callback_data=f"add_cart_{product_id}"
    )
    btn2 = InlineKeyboardButton("🔙 Back to Products", callback_data="menu_products")
    keyboard.add(btn1, btn2)
    return keyboard


def create_cart_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✅ Checkout", callback_data="checkout")
    btn2 = InlineKeyboardButton("🗑️ Clear Cart", callback_data="clear_cart")
    btn3 = InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")
    keyboard.add(btn1, btn2, btn3)
    return keyboard


def create_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("📦 Products")
    btn2 = KeyboardButton("🛒 Cart")
    btn3 = KeyboardButton("📋 Orders")
    btn4 = KeyboardButton("👤 Profile")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def create_order_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("📦 Track Order", callback_data="track_order")
    btn2 = InlineKeyboardButton("✅ Receive Order", callback_data="receive_order")
    btn3 = InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_main")
    keyboard.add(btn1, btn2, btn3)
    return keyboard


def create_profile_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("📝 Edit Profile", callback_data="edit_profile")
    btn2 = InlineKeyboardButton("📜 Order History", callback_data="order_history")
    btn3 = InlineKeyboardButton("� Restock Products", callback_data="restock_products")
    btn4 = InlineKeyboardButton("�🔙 Back to Menu", callback_data="menu_main")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard


def create_restock_buttons(products):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        btn = InlineKeyboardButton(
            f"📦 {product.name} (ID: {product.id}) - Stock: {product.stock}",
            callback_data=f"restock_{product.id}"
        )
        keyboard.add(btn)
    btn_back = InlineKeyboardButton("🔙 Back to Profile", callback_data="menu_profile")
    keyboard.add(btn_back)
    return keyboard
