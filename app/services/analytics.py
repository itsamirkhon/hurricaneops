from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..db_models import IncidentDB, AssetDB

class AnalyticsService:
    def get_dashboard_stats(self, db: Session):
        # Incident Stats
        total_incidents = db.query(IncidentDB).count()
        active_incidents = db.query(IncidentDB).filter(IncidentDB.status != 'resolved').count()
        resolved_incidents = db.query(IncidentDB).filter(IncidentDB.status == 'resolved').count()
        
        # Calculate Mean Time to Resolution (MTTR)
        # We fetch resolved incidents directly for simplicity in SQLite 
        # (func.avg across datediff might be tricky depending on sqlite version/extensions)
        resolved_objs = db.query(IncidentDB).filter(IncidentDB.status == 'resolved', IncidentDB.resolved_at != None).all()
        
        total_resolution_seconds = 0
        resolved_count_with_time = 0
        
        for inc in resolved_objs:
            if inc.reported_at and inc.resolved_at:
                delta = inc.resolved_at - inc.reported_at
                total_resolution_seconds += delta.total_seconds()
                resolved_count_with_time += 1
                
        avg_resolution_minutes = round((total_resolution_seconds / 60) / resolved_count_with_time) if resolved_count_with_time > 0 else 0
        
        # Asset Stats
        total_assets = db.query(AssetDB).count()
        deployed_assets = db.query(AssetDB).filter(AssetDB.status.in_(['deployed', 'on_scene', 'en_route'])).count()
        utilization_rate = round((deployed_assets / total_assets * 100), 1) if total_assets > 0 else 0
        
        # Incidents by Type
        type_counts = db.query(IncidentDB.type, func.count(IncidentDB.type)).group_by(IncidentDB.type).all()
        incidents_by_type = {t: c for t, c in type_counts}
        
        # Recent Trend (Last 24h, grouped by hour - simplified)
        # For demo, returning simple mock trend if not enough data, 
        # basically count of incidents reported in last few hours
        
        return {
            "incidents": {
                "total": total_incidents,
                "active": active_incidents,
                "resolved": resolved_incidents,
                "by_type": incidents_by_type,
                "avg_resolution_time_mins": avg_resolution_minutes
            },
            "assets": {
                "total": total_assets,
                "deployed": deployed_assets,
                "utilization_rate": utilization_rate
            }
        }

analytics_service = AnalyticsService()
