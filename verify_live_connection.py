import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)
from services.supabase_client import get_supabase_client, get_supabase_credentials
from services.campus_repository import campus_lookup

def verify():
    url, key = get_supabase_credentials()
    print("Supabase URL configured:", bool(url))
    print("Supabase Key configured:", bool(key))

    if not url or not key:
        print("[FAIL] Missing credentials in .env.")
        sys.exit(1)

    # Check key safety (no service_role key)
    try:
        import jwt
        decoded = jwt.decode(key, options={"verify_signature": False})
        role = decoded.get("role")
        print("Key role detected:", role)
        if role == "service_role":
            print("[WARNING] You provided a service_role key. Please replace it with the anon / publishable key.")
    except Exception:
        pass

    try:
        client = get_supabase_client()
        print("[OK] Supabase client initialized.")
    except Exception as e:
        print(f"[FAIL] Could not initialize Supabase client: {type(e).__name__}: {e}")
        sys.exit(1)

    # Test 1: Query `plants` table
    try:
        res = client.table("plants").select("id, common_name, scientific_name").limit(5).execute()
        print(f"[OK] Successfully queried 'plants' table. Found {len(res.data)} records.")
        for r in res.data:
            print(f"     - {r.get('common_name')} ({r.get('scientific_name')})")
    except Exception as e:
        print(f"[FAIL] Query to 'plants' table failed: {type(e).__name__}: {e}")
        print("Note: If the table does not exist yet, make sure you ran 'scripts/setup_supabase.sql' in Supabase SQL Editor.")
        return

    # Test 2: Query `campus_locations` table
    try:
        loc_res = client.table("campus_locations").select("id, location_name").limit(5).execute()
        print(f"[OK] Successfully queried 'campus_locations' table. Found {len(loc_res.data)} records.")
    except Exception as e:
        print(f"[FAIL] Query to 'campus_locations' table failed: {type(e).__name__}: {e}")

    # Test 3: Test campus_lookup() repository function with a known species or dummy query
    try:
        test_species = res.data[0]["scientific_name"] if res.data else "Mangifera indica"
        lookup_result = campus_lookup(test_species)
        if lookup_result:
            print(f"[OK] campus_lookup('{test_species}') succeeded: {lookup_result.get('common_name')}")
            print(f"     Locations linked: {lookup_result.get('locations')}")
        else:
            print(f"[INFO] campus_lookup('{test_species}') returned None (not in database yet).")
    except Exception as e:
        print(f"[FAIL] campus_lookup() failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    verify()
