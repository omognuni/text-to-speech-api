from sqlalchemy import Column, Integer, String
from db import Base

class Audio(Base):
    __tablename__ = 'audio'
    
    