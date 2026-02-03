from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class IncidentDB(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, default=generate_uuid)
    type = Column(String, index=True)
    priority = Column(String, index=True)
    description = Column(String)
    affected_count = Column(Integer, default=1)
    status = Column(String, default="active")
    reported_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Location fields
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String, nullable=True)
    
    # JSON fields for lists
    assigned_assets = Column(JSON, default=list)
    notes = Column(JSON, default=list)

class AssetDB(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    type = Column(String, index=True)
    status = Column(String, default="available")
    capacity = Column(Integer, default=4)
    crew_size = Column(Integer, default=2)
    
    # Assignment
    assigned_incident = Column(String, nullable=True)
    eta_minutes = Column(Integer, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Location fields
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String, nullable=True)

class WeatherDB(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    hurricane_category = Column(Integer)
    wind_speed_mph = Column(Float)
    rainfall_inches = Column(Float)
    storm_surge_feet = Column(Float)
    flood_zones_affected = Column(JSON)
    forecast_summary = Column(String)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # 'admin', 'dispatcher', 'viewer'
