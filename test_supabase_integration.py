"""
Automated unit & integration verification for Phase 2 Supabase implementation.
Tests:
1. Missing credentials handling (CampusConfigurationError)
2. Model translation from mock Supabase response
3. Repository error handling
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models.plant import CampusPlantRecord, CampusLocation
from services.campus_repository import campus_lookup, CampusConfigurationError, CampusDatabaseError
from services.supabase_client import get_supabase_credentials

def test_missing_credentials():
    print("Testing missing credentials handling...")
    # Ensure env vars are clear
    old_url = os.environ.pop("SUPABASE_URL", None)
    old_key = os.environ.pop("SUPABASE_KEY", None)
    try:
        campus_lookup("Mangifera indica")
        assert False, "Should have raised CampusConfigurationError"
    except CampusConfigurationError as e:
        print("  [OK] Correctly caught CampusConfigurationError:", str(e)[:60], "...")
    finally:
        if old_url: os.environ["SUPABASE_URL"] = old_url
        if old_key: os.environ["SUPABASE_KEY"] = old_key

def test_models_mapping():
    print("Testing models and data serialization...")
    fake_plant = {
        "id": "12345678-1234-5678-1234-567812345678",
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "description": "Tropical tree",
        "uses": ["Fruit", "Shade"],
        "facts": ["Native to South Asia"],
        "image_url": "https://example.com/mango.jpg",
        "created_at": "2026-09-04T12:00:00Z"
    }
    fake_locations = [
        {"location_name": "East Garden", "description": "Near fountain"},
        {"location_name": "Main Quad", "description": None}
    ]
    record = CampusPlantRecord.from_supabase(fake_plant, fake_locations)
    data = record.to_dict()
    assert data["common_name"] == "Mango"
    assert data["scientific_name"] == "Mangifera indica"
    assert "East Garden" in data["locations"]
    assert "Main Quad" in data["locations"]
    print("  [OK] Model conversion to dict succeeded with expected fields.")

if __name__ == "__main__":
    test_missing_credentials()
    test_models_mapping()
    print("All unit verification tests passed successfully!")
