import logging
from typing import Optional, Dict, Any, List
from models.plant import CampusPlantRecord
from services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class CampusDatabaseError(Exception):
    """Raised when there is an operational error communicating with the database."""
    pass

class CampusConfigurationError(Exception):
    """Raised when database credentials or configurations are missing."""
    pass

def campus_lookup(scientific_name: str) -> Optional[Dict[str, Any]]:
    """
    Looks up a plant species in the Supabase campus database by scientific name.
    
    Returns:
        A dictionary matching the CampusPlantRecord schema if found.
        None if the plant is not catalogued in the campus database.
        
    Raises:
        CampusConfigurationError: If Supabase credentials are missing.
        CampusDatabaseError: If the database query encounters a connection or runtime failure.
    """
    if not scientific_name or not scientific_name.strip():
        return None

    clean_name = scientific_name.strip()

    try:
        supabase = get_supabase_client()
    except RuntimeError as config_err:
        logger.warning("Supabase configuration error: %s", config_err)
        raise CampusConfigurationError(str(config_err)) from config_err

    try:
        # 1. Query the `plants` table matching scientific_name (case-insensitive)
        response = (
            supabase.table("plants")
            .select("*")
            .ilike("scientific_name", clean_name)
            .limit(1)
            .execute()
        )

        plants_data = response.data
        if not plants_data:
            logger.info("Plant '%s' not found in campus database.", clean_name)
            return None

        plant_row = plants_data[0]
        plant_id = plant_row.get("id")

        # 2. Query the associated `campus_locations`
        locations_response = (
            supabase.table("campus_locations")
            .select("location_name, latitude, longitude, description")
            .eq("plant_id", plant_id)
            .execute()
        )
        locations_rows = locations_response.data or []

        # 3. Build model and return clean dict representation for UI consumption
        record = CampusPlantRecord.from_supabase(plant_row, locations_rows)
        return record.to_dict()

    except (CampusConfigurationError, CampusDatabaseError):
        raise
    except Exception as e:
        logger.error("Error during Supabase campus lookup for '%s': %s", clean_name, type(e).__name__)
        raise CampusDatabaseError(f"Database error querying species: {type(e).__name__}") from e
