"""
Mock test simulating full end-to-end lookup without requiring live Supabase credentials.
Tests:
1. Known plant lookup returns full CampusPlantRecord dictionary
2. Unknown plant species returns None (NOT_CATALOGUED state)
3. Database operational exception triggers CampusDatabaseError
"""

import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from services.campus_repository import campus_lookup, CampusDatabaseError

def test_supabase_flow():
    print("Testing Supabase pipeline with mock client...")
    
    mock_client = MagicMock()

    # Scenario 1: Known plant (Found)
    mock_plants_select = MagicMock()
    mock_client.table.return_value = mock_plants_select
    
    # Setup chain: table("plants").select("*").ilike(...).limit(1).execute()
    mock_ilike = MagicMock()
    mock_plants_select.select.return_value = mock_ilike
    mock_limit = MagicMock()
    mock_ilike.ilike.return_value = mock_limit
    mock_limit.limit.return_value = MagicMock(execute=lambda: MagicMock(data=[{
        "id": "mock-uuid-123",
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "description": "A lush tropical tree.",
        "uses": ["Fruit", "Shade"],
        "facts": ["Native to South Asia"],
        "image_url": "https://example.com/mango.jpg",
        "created_at": "2026-09-04T00:00:00Z"
    }]))

    # Setup locations: table("campus_locations").select(...).eq(...).execute()
    mock_locations_table = MagicMock()
    mock_eq = MagicMock()
    mock_locations_table.select.return_value = mock_eq
    mock_eq.eq.return_value = MagicMock(execute=lambda: MagicMock(data=[
        {"location_name": "East Garden"},
        {"location_name": "Main Block"}
    ]))

    def table_router(table_name):
        if table_name == "plants":
            return mock_plants_select
        elif table_name == "campus_locations":
            return mock_locations_table
        return MagicMock()

    mock_client.table.side_effect = table_router

    with patch("services.campus_repository.get_supabase_client", return_value=mock_client):
        # 1. Found flow
        result = campus_lookup("Mangifera indica")
        assert result is not None, "Expected result to be found"
        assert result["common_name"] == "Mango"
        assert result["locations"] == ["East Garden", "Main Block"]
        print("  [OK] Found flow returns mapped record with locations.")

        # 2. Unknown plant (Not Catalogued) flow
        mock_limit.limit.return_value = MagicMock(execute=lambda: MagicMock(data=[]))
        res_unknown = campus_lookup("Unknown plantus")
        assert res_unknown is None, "Expected None for uncatalogued plant"
        print("  [OK] Unknown plant returns None (triggers NOT_CATALOGUED).")

        # 3. DB failure flow
        mock_limit.limit.return_value = MagicMock(execute=MagicMock(side_effect=Exception("Timeout connection")))
        try:
            campus_lookup("Mangifera indica")
            assert False, "Should have raised CampusDatabaseError"
        except CampusDatabaseError as de:
            print("  [OK] Caught CampusDatabaseError on network failure.")

if __name__ == "__main__":
    test_supabase_flow()
    print("All mock pipeline tests passed!")
