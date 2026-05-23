from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///bot_database.db"

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
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="user")
    button_clicks = relationship("ButtonClick", back_populates="user")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    message_text = Column(String(1000))
    message_type = Column(String(50), default="text")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")


class ButtonClick(Base):
    __tablename__ = "button_clicks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    button_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="button_clicks")


def init_database():
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_session():

    return Session()


def add_user(user_id, username=None, first_name=None, last_name=None):

    session = get_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
        else:
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            session.add(user)
        session.commit()
        print(f"User {user_id} added/updated successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error adding user: {e}")
    finally:
        session.close()


def add_message(user_id, message_text, message_type="text"):
    session = get_session()
    try:
        message = Message(
            user_id=user_id, message_text=message_text, message_type=message_type
        )
        session.add(message)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding message: {e}")
    finally:
        session.close()


def add_button_click(user_id, button_name):
    session = get_session()
    try:
        button_click = ButtonClick(user_id=user_id, button_name=button_name)
        session.add(button_click)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding button click: {e}")
    finally:
        session.close()


def get_user(user_id):
    session = get_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        return user
    finally:
        session.close()


def get_all_users():
    session = get_session()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()


def get_user_messages(user_id):
    session = get_session()
    try:
        messages = session.query(Message).filter_by(user_id=user_id).all()
        return messages
    finally:
        session.close()


def get_button_clicks(user_id):
    session = get_session()
    try:
        clicks = session.query(ButtonClick).filter_by(user_id=user_id).all()
        return clicks
    finally:
        session.close()
