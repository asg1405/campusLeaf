"""
Script to seed the Supabase database with the demo campus plants dataset.

Usage:
    python scripts/seed_demo_data.py
    
Ensure SUPABASE_URL and SUPABASE_KEY are configured in your .env or environment.
"""

import sys
import os

# Add parent directory to sys.path so we can import from services and data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from data.demo_plants import demo_campus_database
from services.supabase_client import get_supabase_client, get_supabase_credentials

def seed_database():
    load_dotenv()
    url, key = get_supabase_credentials()

    if not url or not key:
        print("[ERROR] Supabase credentials not found!")
        print("Please set SUPABASE_URL and SUPABASE_KEY in .env or environment variables.")
        sys.exit(1)

    print(f"Connecting to Supabase at: {url[:20]}...")
    try:
        supabase = get_supabase_client()
    except Exception as e:
        print(f"[ERROR] Could not connect to Supabase: {type(e).__name__}: {e}")
        sys.exit(1)

    print(f"Starting seed process for {len(demo_campus_database)} plants...")

    for plant_info in demo_campus_database:
        common_name = plant_info["common_name"]
        scientific_name = plant_info["scientific_name"]
        family = plant_info["family"]
        description = plant_info["description"]
        uses = plant_info["uses"]
        facts = plant_info["facts"]
        locations = plant_info.get("locations", [])

        # Upsert into `plants` table
        plant_payload = {
            "common_name": common_name,
            "scientific_name": scientific_name,
            "family": family,
            "description": description,
            "uses": uses,
            "facts": facts,
        }

        try:
            # Check if plant exists
            existing = (
                supabase.table("plants")
                .select("id")
                .ilike("scientific_name", scientific_name)
                .execute()
            )

            if existing.data and len(existing.data) > 0:
                plant_id = existing.data[0]["id"]
                # Update record
                supabase.table("plants").update(plant_payload).eq("id", plant_id).execute()
                print(f"  [UPDATED] {common_name} ({scientific_name})")
            else:
                insert_res = supabase.table("plants").insert(plant_payload).execute()
                plant_id = insert_res.data[0]["id"]
                print(f"  [INSERTED] {common_name} ({scientific_name})")

            # Remove old locations for this plant before inserting current ones
            supabase.table("campus_locations").delete().eq("plant_id", plant_id).execute()

            # Insert locations
            for loc in locations:
                loc_payload = {
                    "plant_id": plant_id,
                    "location_name": loc.get("location_name") if isinstance(loc, dict) else str(loc),
                    "description": loc.get("description") if isinstance(loc, dict) else None,
                }
                supabase.table("campus_locations").insert(loc_payload).execute()

            print(f"    - Linked {len(locations)} campus locations")

        except Exception as err:
            print(f"  [FAILED] {common_name} ({scientific_name}): {type(err).__name__}: {err}")

    print("\nDatabase seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
