from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class PlantPrediction:
    """Represents the raw ML prediction result."""
    common_name: str
    scientific_name: str
    confidence: float
    family: str
    description: str
    uses: List[str]

@dataclass
class CampusLocation:
    """Represents a physical location on campus where a plant is found."""
    id: Optional[str] = None
    plant_id: Optional[str] = None
    location_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None

@dataclass
class CampusPlantRecord:
    """Represents a campus catalogued plant record."""
    id: str
    common_name: str
    scientific_name: str
    family: str
    description: str
    uses: List[str] = field(default_factory=list)
    facts: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_supabase(cls, plant_row: Dict[str, Any], locations_rows: Optional[List[Dict[str, Any]]] = None) -> "CampusPlantRecord":
        """Builds a CampusPlantRecord from Supabase plant and location query results."""
        locations_list = []
        if locations_rows:
            locations_list = [
                loc.get("location_name") for loc in locations_rows if loc.get("location_name")
            ]
        
        return cls(
            id=str(plant_row.get("id", "")),
            common_name=plant_row.get("common_name", ""),
            scientific_name=plant_row.get("scientific_name", ""),
            family=plant_row.get("family", ""),
            description=plant_row.get("description", "") or "",
            uses=plant_row.get("uses") or [],
            facts=plant_row.get("facts") or [],
            locations=locations_list,
            image_url=plant_row.get("image_url"),
            created_at=str(plant_row.get("created_at", ""))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts to dictionary for seamless compatibility with UI templates."""
        return {
            "id": self.id,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
            "family": self.family,
            "description": self.description,
            "uses": self.uses,
            "facts": self.facts,
            "locations": self.locations,
            "image_url": self.image_url,
            "created_at": self.created_at,
        }
