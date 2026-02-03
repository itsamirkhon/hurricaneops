"""
Simulated real-time data feeds for the Emergency Coordination System.
Provides mock data for incidents, assets, weather, and flood conditions.
"""
import random
from datetime import datetime
from typing import List, Dict
from ..models import (
    Incident, Asset, Location, WeatherData,
    IncidentType, Priority, AssetType, AssetStatus
)


from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, Base
from ..db_models import IncidentDB, AssetDB, WeatherDB
from ..models import (
    Incident, Asset, Location, WeatherData,
    IncidentType, Priority, AssetType, AssetStatus
)
import random
from datetime import datetime
from typing import List, Dict

# Create tables
Base.metadata.create_all(bind=engine)

class DataFeedService:
    """Service providing simulated real-time data feeds using SQLite database."""
    
    def __init__(self):
        self._initialize_demo_data()
    
    def get_db(self):
        return SessionLocal()
        
    def _initialize_demo_data(self):
        """Initialize demo data if database is empty."""
        db = self.get_db()
        try:
            # Check if data exists
            if db.query(IncidentDB).first():
                return

            # Create demo incidents
            demo_incidents = [
                IncidentDB(
                    id="INC-001",
                    type=IncidentType.FLOOD_RESCUE,
                    priority=Priority.CRITICAL,
                    description="Multiple families trapped on rooftops, water level rising rapidly",
                    affected_count=12,
                    latitude=27.9506,
                    longitude=-82.4572,
                    address="Downtown Tampa - Bayshore Blvd",
                    status="active"
                ),
                IncidentDB(
                    id="INC-002",
                    type=IncidentType.MEDICAL_EMERGENCY,
                    priority=Priority.CRITICAL,
                    description="Dialysis patient requires evacuation, power failure imminent",
                    affected_count=1,
                    latitude=27.9659,
                    longitude=-82.4305,
                    address="Tampa General Hospital Area",
                    status="active"
                ),
                IncidentDB(
                    id="INC-003",
                    type=IncidentType.FLOOD_RESCUE,
                    priority=Priority.HIGH,
                    description="Elderly residents trapped in assisted living facility",
                    affected_count=8,
                    latitude=27.9402,
                    longitude=-82.4566,
                    address="South Tampa - Swann Ave",
                    status="active"
                ),
                IncidentDB(
                    id="INC-004",
                    type=IncidentType.STRUCTURAL_COLLAPSE,
                    priority=Priority.HIGH,
                    description="Partial roof collapse at apartment complex, injuries reported",
                    affected_count=5,
                    latitude=27.9825,
                    longitude=-82.4614,
                    address="Carrollwood - Dale Mabry",
                    status="active"
                ),
                IncidentDB(
                    id="INC-005",
                    type=IncidentType.EVACUATION,
                    priority=Priority.MEDIUM,
                    description="Residents in mandatory evacuation zone refusing to leave",
                    affected_count=20,
                    latitude=27.8985,
                    longitude=-82.5145,
                    address="MacDill AFB Area",
                    status="active"
                ),
                IncidentDB(
                    id="INC-006",
                    type=IncidentType.ROAD_BLOCKAGE,
                    priority=Priority.MEDIUM,
                    description="Major debris blocking evacuation route, tree and power lines down",
                    affected_count=0,
                    latitude=27.9547,
                    longitude=-82.4324,
                    address="I-275 at Howard Ave Exit",
                    status="active"
                ),
            ]
            
            for inc in demo_incidents:
                db.add(inc)
            
            # Create demo assets
            demo_assets = [
                AssetDB(
                    id="BOAT-001",
                    name="Rescue Boat Alpha",
                    type=AssetType.BOAT,
                    status=AssetStatus.AVAILABLE,
                    capacity=8,
                    crew_size=3,
                    latitude=27.9420,
                    longitude=-82.4587,
                    address="Davis Islands Marina"
                ),
                AssetDB(
                    id="BOAT-002",
                    name="Rescue Boat Bravo",
                    type=AssetType.BOAT,
                    status=AssetStatus.DEPLOYED,
                    capacity=6,
                    crew_size=2,
                    latitude=27.9506,
                    longitude=-82.4572,
                    address="En route to INC-001",
                    assigned_incident="INC-001",
                    eta_minutes=5
                ),
                AssetDB(
                    id="BOAT-003",
                    name="Rescue Boat Charlie",
                    type=AssetType.BOAT,
                    status=AssetStatus.AVAILABLE,
                    capacity=10,
                    crew_size=4,
                    latitude=27.9340,
                    longitude=-82.4520,
                    address="Ballast Point"
                ),
                AssetDB(
                    id="HELI-001",
                    name="MedEvac Helicopter 1",
                    type=AssetType.HELICOPTER,
                    status=AssetStatus.AVAILABLE,
                    capacity=4,
                    crew_size=3,
                    latitude=27.9659,
                    longitude=-82.4305,
                    address="Tampa General Helipad"
                ),
                AssetDB(
                    id="HELI-002",
                    name="Rescue Helicopter 2",
                    type=AssetType.HELICOPTER,
                    status=AssetStatus.EN_ROUTE,
                    capacity=6,
                    crew_size=4,
                    latitude=27.9600,
                    longitude=-82.4400,
                    address="Airborne",
                    assigned_incident="INC-004",
                    eta_minutes=8
                ),
                AssetDB(
                    id="VEH-001",
                    name="Rescue Unit 1",
                    type=AssetType.GROUND_VEHICLE,
                    status=AssetStatus.AVAILABLE,
                    capacity=6,
                    crew_size=4,
                    latitude=27.9700,
                    longitude=-82.4500,
                    address="Fire Station 1"
                ),
                AssetDB(
                    id="VEH-002",
                    name="Rescue Unit 2",
                    type=AssetType.GROUND_VEHICLE,
                    status=AssetStatus.AVAILABLE,
                    capacity=6,
                    crew_size=4,
                    latitude=27.9800,
                    longitude=-82.4600,
                    address="Fire Station 7"
                ),
                AssetDB(
                    id="VEH-003",
                    name="Medical Response Unit",
                    type=AssetType.GROUND_VEHICLE,
                    status=AssetStatus.DEPLOYED,
                    capacity=2,
                    crew_size=3,
                    latitude=27.9659,
                    longitude=-82.4305,
                    address="Tampa General",
                    assigned_incident="INC-002"
                ),
                AssetDB(
                    id="DRONE-001",
                    name="Surveillance Drone Alpha",
                    type=AssetType.DRONE,
                    status=AssetStatus.DEPLOYED,
                    capacity=0,
                    crew_size=1,
                    latitude=27.9500,
                    longitude=-82.4550,
                    address="Airborne - Downtown",
                    assigned_incident="INC-001"
                ),
                AssetDB(
                    id="DRONE-002",
                    name="Surveillance Drone Bravo",
                    type=AssetType.DRONE,
                    status=AssetStatus.AVAILABLE,
                    capacity=0,
                    crew_size=1,
                    latitude=27.9700,
                    longitude=-82.4500,
                    address="Fire Station 1"
                ),
                AssetDB(
                    id="MED-001",
                    name="Medical Team Alpha",
                    type=AssetType.MEDICAL_TEAM,
                    status=AssetStatus.AVAILABLE,
                    capacity=10,
                    crew_size=5,
                    latitude=27.9659,
                    longitude=-82.4305,
                    address="Tampa General"
                ),
                AssetDB(
                    id="RES-001",
                    name="Swift Water Rescue Team",
                    type=AssetType.RESCUE_TEAM,
                    status=AssetStatus.AVAILABLE,
                    capacity=0,
                    crew_size=6,
                    latitude=27.9420,
                    longitude=-82.4587,
                    address="Davis Islands"
                ),
            ]
            
            for asset in demo_assets:
                db.add(asset)

             # Initialize weather
            weather = WeatherDB(
                hurricane_category=3,
                wind_speed_mph=120,
                rainfall_inches=8.5,
                storm_surge_feet=6.2,
                flood_zones_affected=["Zone A", "Zone B", "Zone C", "Zone AE"],
                forecast_summary="Category 3 Hurricane making landfall. Peak storm surge expected within 2 hours. Conditions deteriorating."
            )
            db.add(weather)
            
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error initializing data: {e}")
        finally:
            db.close()
    
    def _to_incident_model(self, db_obj: IncidentDB) -> Incident:
        if not db_obj: return None
        return Incident(
            id=db_obj.id,
            type=db_obj.type,
            priority=db_obj.priority,
            location=Location(latitude=db_obj.latitude, longitude=db_obj.longitude, address=db_obj.address),
            description=db_obj.description,
            affected_count=db_obj.affected_count,
            status=db_obj.status,
            reported_at=db_obj.reported_at,
            assigned_assets=db_obj.assigned_assets or [],
            notes=db_obj.notes or []
        )

    def _to_asset_model(self, db_obj: AssetDB) -> Asset:
        if not db_obj: return None
        return Asset(
            id=db_obj.id,
            name=db_obj.name,
            type=db_obj.type,
            status=db_obj.status,
            location=Location(latitude=db_obj.latitude, longitude=db_obj.longitude, address=db_obj.address),
            capacity=db_obj.capacity,
            crew_size=db_obj.crew_size,
            assigned_incident=db_obj.assigned_incident,
            eta_minutes=db_obj.eta_minutes,
            last_updated=db_obj.last_updated
        )

    def _to_weather_model(self, db_obj: WeatherDB) -> WeatherData:
        if not db_obj: return None
        return WeatherData(
            timestamp=db_obj.timestamp,
            hurricane_category=db_obj.hurricane_category,
            wind_speed_mph=db_obj.wind_speed_mph,
            rainfall_inches=db_obj.rainfall_inches,
            storm_surge_feet=db_obj.storm_surge_feet,
            flood_zones_affected=db_obj.flood_zones_affected or [],
            forecast_summary=db_obj.forecast_summary
        )

    # --- Incident Methods ---
    def get_all_incidents(self) -> List[Incident]:
        db = self.get_db()
        try:
            incidents = db.query(IncidentDB).all()
            return [self._to_incident_model(i) for i in incidents]
        finally:
            db.close()
    
    def get_incident(self, incident_id: str) -> Incident:
        db = self.get_db()
        try:
            incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
            return self._to_incident_model(incident)
        finally:
            db.close()
    
    def add_incident(self, incident: Incident) -> Incident:
        db = self.get_db()
        try:
            db_obj = IncidentDB(
                id=incident.id,
                type=incident.type,
                priority=incident.priority,
                description=incident.description,
                affected_count=incident.affected_count,
                latitude=incident.location.latitude,
                longitude=incident.location.longitude,
                address=incident.location.address,
                status=incident.status,
                reported_at=incident.reported_at,
                assigned_assets=incident.assigned_assets,
                notes=incident.notes
            )
            db.add(db_obj)
            db.commit()
            return incident
        finally:
            db.close()
    
    def update_incident(self, incident_id: str, updates: dict) -> Incident:
        db = self.get_db()
        try:
            db_obj = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
            if db_obj:
                for key, value in updates.items():
                    if key == 'location':
                        # Handle location update specially
                         if isinstance(value, dict):
                            if 'latitude' in value: db_obj.latitude = value['latitude']
                            if 'longitude' in value: db_obj.longitude = value['longitude']
                            if 'address' in value: db_obj.address = value['address']
                         else: # Assumed object
                            db_obj.latitude = value.latitude
                            db_obj.longitude = value.longitude
                            db_obj.address = value.address
                    elif hasattr(db_obj, key):
                        setattr(db_obj, key, value)
                db.commit()
                db.refresh(db_obj)
            return self._to_incident_model(db_obj)
        finally:
            db.close()
    
    def delete_incident(self, incident_id: str) -> bool:
        db = self.get_db()
        try:
            db_obj = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
            if db_obj:
                db.delete(db_obj)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    # --- Asset Methods ---
    def get_all_assets(self) -> List[Asset]:
        db = self.get_db()
        try:
            assets = db.query(AssetDB).all()
            return [self._to_asset_model(a) for a in assets]
        finally:
            db.close()
    
    def get_asset(self, asset_id: str) -> Asset:
        db = self.get_db()
        try:
            asset = db.query(AssetDB).filter(AssetDB.id == asset_id).first()
            return self._to_asset_model(asset)
        finally:
            db.close()
    
    def get_available_assets(self) -> List[Asset]:
        db = self.get_db()
        try:
            assets = db.query(AssetDB).filter(AssetDB.status == "available").all()
            return [self._to_asset_model(a) for a in assets]
        finally:
            db.close()
    
    def update_asset(self, asset_id: str, updates: dict) -> Asset:
        db = self.get_db()
        try:
            db_obj = db.query(AssetDB).filter(AssetDB.id == asset_id).first()
            if db_obj:
                for key, value in updates.items():
                    if key == 'location':
                         if isinstance(value, dict):
                            if 'latitude' in value: db_obj.latitude = value['latitude']
                            if 'longitude' in value: db_obj.longitude = value['longitude']
                            if 'address' in value: db_obj.address = value['address']
                         else:
                            db_obj.latitude = value.latitude
                            db_obj.longitude = value.longitude
                            db_obj.address = value.address
                    elif hasattr(db_obj, key):
                        setattr(db_obj, key, value)
                db_obj.last_updated = datetime.utcnow()
                db.commit()
                db.refresh(db_obj)
            return self._to_asset_model(db_obj)
        finally:
            db.close()
    
    def assign_asset(self, asset_id: str, incident_id: str, eta_minutes: int = None) -> Asset:
        return self.update_asset(asset_id, {
            "status": "en_route", # Use string matching DB defaults
            "assigned_incident": incident_id,
            "eta_minutes": eta_minutes or random.randint(5, 20)
        })
    
    def release_asset(self, asset_id: str) -> Asset:
        return self.update_asset(asset_id, {
            "status": "available",
            "assigned_incident": None,
            "eta_minutes": None
        })
    
    # --- Weather Methods ---
    def get_weather(self) -> WeatherData:
        db = self.get_db()
        try:
            weather = db.query(WeatherDB).order_by(WeatherDB.timestamp.desc()).first()
            
            # Simulate slight variations if weather exists
            if weather:
                 # In a real app we'd trigger a new reading or logic here, 
                 # for now let's just update the DB object slightly to mimic the original 'live' feel
                 weather.wind_speed_mph += random.uniform(-0.5, 0.5)
                 weather.storm_surge_feet += random.uniform(-0.05, 0.05)
                 weather.timestamp = datetime.utcnow()
                 db.commit()
                 
            return self._to_weather_model(weather)
        finally:
            db.close()
    
    def get_summary_stats(self) -> dict:
        db = self.get_db()
        try:
            total_incidents = db.query(IncidentDB).count()
            critical_incidents = db.query(IncidentDB).filter(IncidentDB.priority == "critical").count()
            high_priority = db.query(IncidentDB).filter(IncidentDB.priority == "high").count()
            
            total_assets = db.query(AssetDB).count()
            available_assets = db.query(AssetDB).filter(AssetDB.status == "available").count()
            deployed_assets = db.query(AssetDB).filter(AssetDB.status.in_(["deployed", "en_route", "on_scene"])).count()
            
            incidents = db.query(IncidentDB).all()
            total_affected = sum(i.affected_count for i in incidents)
            
            weather = db.query(WeatherDB).order_by(WeatherDB.timestamp.desc()).first()
            weather_data = {
                 "hurricane_category": 0,
                 "wind_speed_mph": 0,
                 "storm_surge_feet": 0
            }
            if weather:
                weather_data = {
                    "hurricane_category": weather.hurricane_category,
                    "wind_speed_mph": round(weather.wind_speed_mph),
                    "storm_surge_feet": round(weather.storm_surge_feet, 1)
                }

            return {
                "total_incidents": total_incidents,
                "critical_incidents": critical_incidents,
                "high_priority_incidents": high_priority,
                "total_assets": total_assets,
                "available_assets": available_assets,
                "deployed_assets": deployed_assets,
                "total_affected": total_affected,
                "weather": weather_data
            }
        finally:
            db.close()


# Singleton instance
data_feed_service = DataFeedService()
