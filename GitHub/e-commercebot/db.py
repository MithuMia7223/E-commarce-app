from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///ecommerce.db"

engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    product_number = Column(String(50))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    shipping_address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


def init_database():
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_session():
    return Session()


def add_user(user_id, username=None, first_name=None, last_name=None, phone=None):
    session = get_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
            )
            session.add(user)
            session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
    finally:
        session.close()


def add_product(name, description, price, stock, product_number=None, image_url=None):
    session = get_session()
    try:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            product_number=product_number,
            image_url=image_url,
        )
        session.add(product)
        session.commit()
        return product
    except Exception as e:
        session.rollback()
        print(f"Error adding product: {e}")
    finally:
        session.close()


def get_all_products():
    session = get_session()
    try:
        products = session.query(Product).all()
        return products
    finally:
        session.close()


def get_product(product_id):
    session = get_session()
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        return product
    finally:
        session.close()


def add_to_cart(user_id, product_id, quantity=1):
    session = get_session()
    try:
        cart_item = (
            session.query(Cart)
            .filter_by(user_id=user_id, product_id=product_id)
            .first()
        )
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(cart_item)
        session.commit()
        return cart_item
    except Exception as e:
        session.rollback()
        print(f"Error adding to cart: {e}")
    finally:
        session.close()


def get_cart(user_id):
    session = get_session()
    try:
        cart_items = session.query(Cart).filter_by(user_id=user_id).all()
        return cart_items
    finally:
        session.close()


def create_order(user_id, shipping_address):
    session = get_session()
    try:
        cart_items = get_cart(user_id)
        if not cart_items:
            return None

        total_amount = 0
        for item in cart_items:
            product = get_product(item.product_id)
            total_amount += product.price * item.quantity

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
        )
        session.add(order)
        session.commit()

        for item in cart_items:
            product = get_product(item.product_id)
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price,
            )
            session.add(order_item)
            session.delete(item)

        session.commit()
        return order
    except Exception as e:
        session.rollback()
        print(f"Error creating order: {e}")
    finally:
        session.close()


def update_product_stock(product_id, new_stock):
    session = get_session()
    try:
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            product.stock = new_stock
            session.commit()
            return product
    except Exception as e:
        session.rollback()
        print(f"Error updating product stock: {e}")
    finally:
        session.close()
