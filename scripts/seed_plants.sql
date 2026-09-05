-- ==============================================================================
-- Campus Plant ID - Seed Data SQL Script
-- ==============================================================================
-- Run this directly in the Supabase SQL Editor.
-- Running as SQL in the editor executes with admin privileges and bypasses RLS.

DO $$
DECLARE
    mango_id UUID;
    neem_id UUID;
    monstera_id UUID;
    ficus_id UUID;
    lavender_id UUID;
    ginkgo_id UUID;
BEGIN
    -- 1. Insert / Upsert Mango
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'Mango',
        'Mangifera indica',
        'Anacardiaceae',
        'A tropical evergreen tree with long, glossy leaves and edible fruit.',
        ARRAY['Fruit', 'Shade', 'Ornamental'],
        ARRAY['Evergreen tree', 'Family: Anacardiaceae', 'Native to South Asia']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO mango_id;

    DELETE FROM public.campus_locations WHERE plant_id = mango_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (mango_id, 'East Garden', 'Near the central fountain path'),
    (mango_id, 'Near Main Block', 'Lawn adjacent to Room 102');

    -- 2. Insert / Upsert Neem
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'Neem',
        'Azadirachta indica',
        'Meliaceae',
        'A fast-growing tree noted for its drought resistance and medicinal properties.',
        ARRAY['Medicinal', 'Shade', 'Pesticide'],
        ARRAY['Evergreen tree', 'Family: Meliaceae', 'Native to the Indian subcontinent']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO neem_id;

    DELETE FROM public.campus_locations WHERE plant_id = neem_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (neem_id, 'North Gate', 'Bordering the visitor security booth'),
    (neem_id, 'Library Courtyard', 'Inner shaded seating quad');

    -- 3. Insert / Upsert Swiss Cheese Plant
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'Swiss Cheese Plant',
        'Monstera deliciosa',
        'Araceae',
        'An evergreen climbing vine famous for its broad, perforate and fenestrated leaves.',
        ARRAY['Ornamental', 'Air Purification', 'Indoor Greenery'],
        ARRAY['Hemi-epiphytic climber', 'Family: Araceae', 'Native to tropical rainforests of Central America']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO monstera_id;

    DELETE FROM public.campus_locations WHERE plant_id = monstera_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (monstera_id, 'Science Block Atrium', 'Indoor garden bed near reception'),
    (monstera_id, 'Greenhouse Bay 2', 'Climbing trellis section');

    -- 4. Insert / Upsert Fiddle-leaf Fig
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'Fiddle-leaf Fig',
        'Ficus lyrata',
        'Moraceae',
        'A popular species of flowering plant with broad, violin-shaped foliage.',
        ARRAY['Ornamental', 'Interior Design', 'Architectural Foliage'],
        ARRAY['Banyan fig group', 'Family: Moraceae', 'Native to western Africa']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO ficus_id;

    DELETE FROM public.campus_locations WHERE plant_id = ficus_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (ficus_id, 'Administration Lobby', 'Main entrance lightwell');

    -- 5. Insert / Upsert English Lavender
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'English Lavender',
        'Lavandula angustifolia',
        'Lamiaceae',
        'A flowering plant valued for sweet aromatic foliage and striking violet flowers.',
        ARRAY['Essential Oils', 'Pollinator Attraction', 'Culinary & Herbal'],
        ARRAY['Subshrub herb', 'Family: Lamiaceae', 'Native to the Mediterranean region']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO lavender_id;

    DELETE FROM public.campus_locations WHERE plant_id = lavender_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (lavender_id, 'Botanical Herb Garden', 'Raised stone bed #3');

    -- 6. Insert / Upsert Maidenhair Tree
    INSERT INTO public.plants (common_name, scientific_name, family, description, uses, facts)
    VALUES (
        'Maidenhair Tree',
        'Ginkgo biloba',
        'Ginkgoaceae',
        'A living fossil with distinct fan-shaped deciduous leaves that turn golden yellow in autumn.',
        ARRAY['Medicinal Extract', 'Urban Shade', 'Botanical Teaching'],
        ARRAY['Living fossil with no close living relatives', 'Family: Ginkgoaceae', 'Native to China']
    )
    ON CONFLICT (scientific_name) DO UPDATE 
    SET common_name = EXCLUDED.common_name,
        family = EXCLUDED.family,
        description = EXCLUDED.description,
        uses = EXCLUDED.uses,
        facts = EXCLUDED.facts
    RETURNING id INTO ginkgo_id;

    DELETE FROM public.campus_locations WHERE plant_id = ginkgo_id;
    INSERT INTO public.campus_locations (plant_id, location_name, description) VALUES
    (ginkgo_id, 'Old Quadrangle', 'South-west heritage pathway');

END $$;
