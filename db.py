


from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    phone_number = Column(String, primary_key=True)
    message_type = Column(Enum('ask', 'image', 'friend', name='messagetype'), nullable=False)
    username = Column(String)
    chat_id = Column(String)
    country_code = Column(String)
    phone = Column(String)
    language_code = Column(String)
    total_messages = Column(Integer)
    last_activity = Column(DateTime)
    created_at = Column(DateTime)
    utm_content = Column(String)
    utm_source = Column(String)
    utm_medium = Column(String)
    utm_campaign = Column(String)
    message_limit = Column(Integer)
    image_limit = Column(Integer)
    total_image_generation = Column(Integer)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_phone_number = Column(String, ForeignKey('users.phone_number'))
    content = Column(String)
    message_type = Column(Enum('ask', 'image', 'friend', name='messagetype'), nullable=False)  # New field
    created_at = Column(DateTime)


# db_url = 'postgresql://postgres:mysecretpassword@localhost:5432/test'

# engine = create_engine(db_url)

# Base.metadata.create_all(engine)