from config import API_TOKEN
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import (
    init_database,
    add_user,
    get_all_products,
    get_product,
    add_to_cart,
    get_cart,
    create_order,
    update_product_stock,
)
from buttons import (
    create_welcome_buttons,
    create_order_buttons,
    create_cart_buttons,
    create_profile_buttons,
    create_product_detail_buttons,
    create_restock_buttons,
)

init_database()

bot = telebot.TeleBot(token=API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    add_user(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    keyboard = create_welcome_buttons()
    bot.send_message(
        message.chat.id,
        "Welcome to E-Commerce Bot! 🛒",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["products"])
def show_products(message):
    products = get_all_products()
    if not products:
        bot.send_message(message.chat.id, "No products available.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        button = InlineKeyboardButton(
            text=f"{product.name} - ${product.price}",
            callback_data=f"product_{product.id}",
        )
        keyboard.add(button)

    bot.send_message(message.chat.id, "Available Products:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def show_product_details(call):
    try:
        product_id = int(call.data.split("_")[1])
        product = get_product(product_id)

        if product:
            keyboard = create_product_detail_buttons(product.id)

            message = f"Product: {product.name}\nPrice: ${product.price}\nStock: {product.stock}\n\n{product.description}"
            bot.send_message(call.message.chat.id, message, reply_markup=keyboard)
            bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in show_product_details: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "menu_products")
def menu_products_handler(call):
    try:
        products = get_all_products()
        if not products:
            bot.send_message(call.message.chat.id, "No products available.")
            bot.answer_callback_query(call.id)
            return

        keyboard = InlineKeyboardMarkup(row_width=1)
        for product in products:
            button = InlineKeyboardButton(
                text=f"{product.name} - ${product.price}",
                callback_data=f"product_{product.id}",
            )
            keyboard.add(button)

        bot.send_message(
            call.message.chat.id, "Available Products:", reply_markup=keyboard
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in menu_products_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "menu_cart")
def menu_cart_handler(call):
    try:
        cart_items = get_cart(call.message.chat.id)
        if not cart_items:
            bot.send_message(call.message.chat.id, "Your cart is empty.")
            bot.answer_callback_query(call.id)
            return

        total = 0
        message_text = "🛒 Your Cart:\n\n"
        for item in cart_items:
            product = get_product(item.product_id)
            message_text += (
                f"{product.name} x {item.quantity} - ${product.price * item.quantity}\n"
            )
            total += product.price * item.quantity

        message_text += f"\nTotal: ${total}"

        keyboard = create_cart_buttons()
        bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in menu_cart_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "menu_orders")
def menu_orders_handler(call):
    try:
        keyboard = create_order_buttons()
        bot.send_message(call.message.chat.id, "📋 Your Orders:", reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in menu_orders_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "menu_profile")
def menu_profile_handler(call):
    try:
        keyboard = create_profile_buttons()
        bot.send_message(
            call.message.chat.id,
            "👤 Your Profile:\n\nUsername: User\nPhone: Not set",
            reply_markup=keyboard,
        )
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in menu_profile_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "receive_order")
def receive_order_handler(call):
    try:
        from db import get_session, Order, OrderItem, Product

        session = get_session()
        try:
            orders = session.query(Order).filter_by(user_id=call.message.chat.id).all()
            if not orders:
                bot.send_message(call.message.chat.id, "No orders to receive.")
                bot.answer_callback_query(call.id)
                return

            for order in orders:
                order_items = (
                    session.query(OrderItem).filter_by(order_id=order.id).all()
                )
                message_text = f"📦 Order ID: {order.id}\n\n"
                for item in order_items:
                    product = (
                        session.query(Product).filter_by(id=item.product_id).first()
                    )
                    message_text += f"{product.name} x {item.quantity}\n"
                total_amount = order.total_amount
                status = order.status
                message_text += f"\nTotal: ${total_amount}\nStatus: {status}"

                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(
                    InlineKeyboardButton(
                        "✅ Accept", callback_data=f"accept_order_{order.id}"
                    ),
                    InlineKeyboardButton(
                        "❌ Cancel", callback_data=f"cancel_order_{order.id}"
                    ),
                )

                bot.send_message(
                    call.message.chat.id, message_text, reply_markup=keyboard
                )
            bot.answer_callback_query(call.id)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in receive_order_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_order_"))
def accept_order_handler(call):
    try:
        order_id = int(call.data.split("_")[2])
        from db import get_session, Order, OrderItem, Product

        session = get_session()
        try:
            order = session.query(Order).filter_by(id=order_id).first()
            if order:
                order.status = "accepted"
                session.commit()

                order_items = (
                    session.query(OrderItem).filter_by(order_id=order.id).all()
                )
                message_text = f"✅ Order Accepted\n\n"
                message_text += f"Order ID: {order.id}\n"
                message_text += f"User ID: {order.user_id}\n"
                message_text += f"Shipping Address: {order.shipping_address}\n"
                message_text += f"Status: {order.status}\n\n"
                message_text += "Products:\n"
                for item in order_items:
                    product = (
                        session.query(Product).filter_by(id=item.product_id).first()
                    )
                    message_text += f"  - Product ID: {product.id}\n"
                    message_text += f"    Name: {product.name}\n"
                    message_text += f"    Quantity: {item.quantity}\n"
                    message_text += f"    Price: ${product.price}\n"
                    message_text += (
                        f"    Subtotal: ${product.price * item.quantity}\n\n"
                    )
                message_text += f"Total: ${order.total_amount}"

                keyboard = InlineKeyboardMarkup(row_width=1)
                keyboard.add(
                    InlineKeyboardButton("📋 Orders", callback_data="menu_orders")
                )
                bot.send_message(
                    call.message.chat.id, message_text, reply_markup=keyboard
                )
            bot.answer_callback_query(call.id)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in accept_order_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_order_"))
def cancel_order_handler(call):
    try:
        order_id = int(call.data.split("_")[2])
        from db import get_session, Order

        session = get_session()
        try:
            order = session.query(Order).filter_by(id=order_id).first()
            if order:
                session.delete(order)
                session.commit()
                bot.send_message(call.message.chat.id, "❌ No data saved")
            bot.answer_callback_query(call.id)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in cancel_order_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "track_order")
def track_order_handler(call):
    try:
        bot.send_message(call.message.chat.id, "📦 Order tracking feature coming soon!")
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in track_order_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
def clear_cart_handler(call):
    try:
        from db import get_session, Cart

        session = get_session()
        try:
            session.query(Cart).filter_by(user_id=call.message.chat.id).delete()
            session.commit()
            bot.send_message(call.message.chat.id, "🗑️ Cart cleared!")
            bot.answer_callback_query(call.id)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in clear_cart_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "menu_main")
def menu_main_handler(call):
    try:
        keyboard = create_welcome_buttons()
        bot.send_message(call.message.chat.id, "🏠 Main Menu:", reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in menu_main_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "edit_profile")
def edit_profile_handler(call):
    try:
        bot.send_message(call.message.chat.id, "📝 Edit profile feature coming soon!")
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in edit_profile_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "order_history")
def order_history_handler(call):
    try:
        from db import get_session, Order, OrderItem, Product

        session = get_session()
        try:
            orders = session.query(Order).filter_by(user_id=call.message.chat.id).all()
            if not orders:
                bot.send_message(call.message.chat.id, "📜 No order history yet.")
                bot.answer_callback_query(call.id)
                return

            message_text = "📜 Order History:\n\n"
            for order in orders:
                message_text += (
                    f"Order ID: {order.id} - ${order.total_amount} - {order.status}\n"
                )
            bot.send_message(call.message.chat.id, message_text)
            bot.answer_callback_query(call.id)
        finally:
            session.close()
    except Exception as e:
        print(f"Error in order_history_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_cart_"))
def add_to_cart_handler(call):
    try:
        product_id = int(call.data.split("_")[2])
        add_to_cart(call.message.chat.id, product_id)
        bot.answer_callback_query(call.id, "Added to cart!")
    except Exception as e:
        print(f"Error in add_to_cart_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.message_handler(commands=["cart"])
def show_cart(message):
    cart_items = get_cart(message.chat.id)
    if not cart_items:
        bot.send_message(message.chat.id, "Your cart is empty.")
        return

    total = 0
    message_text = "🛒 Your Cart:\n\n"
    for item in cart_items:
        product = get_product(item.product_id)
        message_text += (
            f"{product.name} x {item.quantity} - ${product.price * item.quantity}\n"
        )
        total += product.price * item.quantity

    message_text += f"\nTotal: ${total}"

    keyboard = create_cart_buttons()
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def start_checkout(call):
    try:
        bot.send_message(
            call.message.chat.id,
            "Please enter your shipping address:",
        )
        bot.register_next_step_handler(call.message, process_address)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in start_checkout: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data == "restock_products")
def restock_products_handler(call):
    try:
        products = get_all_products()
        if not products:
            bot.send_message(call.message.chat.id, "No products available.")
            bot.answer_callback_query(call.id)
            return

        keyboard = create_restock_buttons(products)
        message_text = "📦 Restock Products\n\nClick on a product to restock:\n\n"
        for product in products:
            message_text += (
                f"ID: {product.id} - {product.name} - Stock: {product.stock}\n"
            )

        bot.send_message(call.message.chat.id, message_text, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in restock_products_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("restock_"))
def restock_product_handler(call):
    try:
        product_id = int(call.data.split("_")[1])
        product = get_product(product_id)

        if product:
            message_text = f"📦 Restock: {product.name}\n\n"
            message_text += f"Current Stock: {product.stock}\n\n"
            message_text += "Please enter the new stock quantity:"

            bot.send_message(call.message.chat.id, message_text)
            bot.register_next_step_handler(call.message, process_restock, product_id)
            bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error in restock_product_handler: {e}")
        try:
            bot.answer_callback_query(call.id)
        except:
            pass


def process_restock(message, product_id):
    try:
        new_stock = int(message.text)
        if new_stock < 0:
            bot.send_message(
                message.chat.id, "Stock cannot be negative. Please try again."
            )
            return

        update_product_stock(product_id, new_stock)
        product = get_product(product_id)
        bot.send_message(
            message.chat.id,
            f"✅ Stock updated successfully!\n\nProduct: {product.name}\nNew Stock: {product.stock}",
        )
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number. Try again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error updating stock: {e}")


def process_address(message):
    shipping_address = message.text
    order = create_order(message.chat.id, shipping_address)

    if order:
        bot.send_message(
            message.chat.id,
            f"Order created successfully!\nOrder ID: {order.id}\nTotal: ${order.total_amount}\nStatus: {order.status}",
        )
    else:
        bot.send_message(message.chat.id, "Your cart is empty.")


bot.polling()
