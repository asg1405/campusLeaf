-- ==============================================================================
-- Campus Plant ID - Database Schema (Phase 2)
-- ==============================================================================
-- Run this script in the Supabase SQL Editor to initialize tables and indexes.

-- 1. Enable UUID generation extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Create `plants` table
CREATE TABLE IF NOT EXISTS public.plants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    common_name TEXT NOT NULL,
    scientific_name TEXT NOT NULL UNIQUE,
    family TEXT NOT NULL,
    description TEXT,
    uses TEXT[] DEFAULT '{}',
    facts TEXT[] DEFAULT '{}',
    image_url TEXT, -- Ready for Supabase Storage in future phases
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 3. Create `campus_locations` table (One-to-Many with plants)
CREATE TABLE IF NOT EXISTS public.campus_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id UUID NOT NULL REFERENCES public.plants(id) ON DELETE CASCADE,
    location_name TEXT NOT NULL,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 4. Create Indexes for efficient lookup
CREATE INDEX IF NOT EXISTS idx_plants_scientific_name ON public.plants (LOWER(scientific_name));
CREATE INDEX IF NOT EXISTS idx_campus_locations_plant_id ON public.campus_locations (plant_id);

-- 5. Automatically update `updated_at` on modification of plants
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS trigger_plants_updated_at ON public.plants;
CREATE TRIGGER trigger_plants_updated_at
    BEFORE UPDATE ON public.plants
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) and grant read access to anon
ALTER TABLE public.plants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.campus_locations ENABLE ROW LEVEL SECURITY;

-- Allow public read access to plants and campus locations
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE tablename = 'plants' AND policyname = 'Allow public read plants'
    ) THEN
        CREATE POLICY "Allow public read plants" ON public.plants FOR SELECT USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE tablename = 'campus_locations' AND policyname = 'Allow public read locations'
    ) THEN
        CREATE POLICY "Allow public read locations" ON public.campus_locations FOR SELECT USING (true);
    END IF;
END
$$;
