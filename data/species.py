# CampusLeaf static design data — port of the androidDesign React data layer
# (src/data/speciesData.ts, src/data/sampleLeaves.ts, src/data/researchData.ts).
# This is PRESENTATION content only. Supabase remains the source of truth for
# live campus records; nothing here is written to the database.

MCE_CAMPUS_CENTER = {
    "lat": 12.9815,
    "lng": 76.0965,
    "zoom": 17,
    "campus_name": "Malnad College of Engineering (MCE)",
    "city": "Hassan, Karnataka - 573201",
}

# Display order follows the design (Pongam first). This is presentation order
# only and is unrelated to the trained model's output-index mapping, which
# lives in services/plant_identifier.py and must not be changed here.
MCE_SPECIES = [
    {
        "id": 1,
        "species_id": 1,
        "common_name": "Pongam / Indian Beech",
        "scientific_name": "Pongamia pinnata",
        "family": "Fabaceae",
        "kannada_name": "ಹೊಂಗೆ ಮರ (Honge Mara)",
        "description": "Fast-growing multipurpose nitrogen-fixing tree famous across Karnataka for biodiesel seeds and dense cooling shade. Extensively studied in campus agroforestry.",
        "habitat": "Open-air theatre periphery, campus avenues, and parking zones",
        "leaf_morphology": "Odd-pinnate compound leaves with 5–9 glossy, ovate-elliptic leaflets and prominent pale venation.",
        "flowering_season": "April to June (White to pink-purple pea-like fragrant flowers)",
        "ecological_significance": "Major indigenous biofuel source; soil nitrogen replenisher and robust microclimate cooling canopy.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSomrqqtO6xV4SQ1-frt-89xIEThglznJ-XfBjHyCvGPcgbe9JTDZydVq93&s=10",
        "latitude": 12.9814,
        "longitude": 76.0955,
        "location_description": "Open Air Theatre (OAT) Perimeter Greenery & West Walkway",
        "campus_zone": "Open Air Theatre Zone",
        "is_demo_coords": True,
    },
    {
        "id": 2,
        "species_id": 2,
        "common_name": "Malabar Plum / Jamun",
        "scientific_name": "Syzygium cumini",
        "family": "Myrtaceae",
        "kannada_name": "ನೇರಳೆ ಮರ (Nerale Mara)",
        "description": "Slow-growing, long-lived evergreen tree yielding astringent deep-purple berries known for anti-diabetic virtues and high antioxidant content.",
        "habitat": "Girls Hostel perimeter, water catchment spots, and eastern lawns",
        "leaf_morphology": "Opposite, coriaceous (leathery), oblong-ovate leaves with faint turpentine aroma when crushed and dense parallel secondary veins.",
        "flowering_season": "March to May (Small fragrant greenish-white flowers in cymes)",
        "ecological_significance": "Crucial monsoon fruit feast for campus bats, bulbuls, and squirrels; groundwater stabilizer.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTubVqx8M1z-Pja4jXbm5fNclHJzL1nVycubAnHnbNFdE2tgI6GUyya6f8&s=10",
        "latitude": 12.9806,
        "longitude": 76.0966,
        "location_description": "Girls Hostel Perimeter and East Lawn",
        "campus_zone": "Hostel Enclave",
        "is_demo_coords": True,
    },
    {
        "id": 3,
        "species_id": 3,
        "common_name": "Jackfruit Tree",
        "scientific_name": "Artocarpus heterophyllus",
        "family": "Moraceae",
        "kannada_name": "ಹಲಸಿನ ಮರ (Halasina Mara)",
        "description": "Tropical evergreen tree indigenous to the Western Ghats producing the largest tree-borne fruit in the world. Deeply rooted in Malnad Karnataka heritage.",
        "habitat": "Hostel surroundings, moisture-retaining groves, and botanical gardens",
        "leaf_morphology": "Stiff, glossy dark-green obovate to elliptic leaves with entire margins, prominent midrib, and leathery texture.",
        "flowering_season": "December to March (Cauliflorous flowering directly on trunk and older branches)",
        "ecological_significance": "Vital nutrition source for local campus wildlife and traditional agroforestry heritage of Malnad Karnataka.",
        "image_url": "https://m.media-amazon.com/images/I/61uRrl9kpML._AC_UF1000,1000_QL80_.jpg",
        "latitude": 12.9804,
        "longitude": 76.0971,
        "location_description": "MCE Boys Hostel Block-A Green Courtyard",
        "campus_zone": "Hostel Enclave",
        "is_demo_coords": True,
    },
    {
        "id": 4,
        "species_id": 4,
        "common_name": "False Ashoka / Mast Tree",
        "scientific_name": "Polyalthia longifolia",
        "family": "Annonaceae",
        "kannada_name": "ಅಶೋಕ ಮರ (Ashoka Mara)",
        "description": "Tall, slender columnar evergreen tree with pendulous branches frequently planted as architectural noise buffers and windbreaks.",
        "habitat": "Boulevards, security perimeter walls, and formal driveway borders",
        "leaf_morphology": "Narrow, lanceolate, long-attenuate leaves with characteristic undulating/wavy margins and shining surface.",
        "flowering_season": "March to April (Delicate star-like pale green flowers in clusters)",
        "ecological_significance": "Acoustic noise reduction, atmospheric dust filtration, and graceful campus architectural lining.",
        "image_url": "https://www.tanarata.net/wp-content/uploads/2025/02/False-ashoka-tree-1-1024x682.jpg",
        "latitude": 12.9821,
        "longitude": 76.0964,
        "location_description": "Along the boundary walls of the Main Administrative Portico",
        "campus_zone": "Main Entrance Avenue",
        "is_demo_coords": True,
    },
]

SAMPLE_LEAVES = [
    {
        "id": 1,
        "species_id": 1,
        "name": "Pongam Leaf (Pongamia pinnata)",
        "scientific_name": "Pongamia pinnata",
        "family": "Fabaceae",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSomrqqtO6xV4SQ1-frt-89xIEThglznJ-XfBjHyCvGPcgbe9JTDZydVq93&s=10",
        "description": "Glossy odd-pinnate leaf with 5–9 leaflets from MCE Open Air Theatre perimeter.",
    },
    {
        "id": 2,
        "species_id": 2,
        "name": "Malabar Plum / Jamun (Syzygium cumini)",
        "scientific_name": "Syzygium cumini",
        "family": "Myrtaceae",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTubVqx8M1z-Pja4jXbm5fNclHJzL1nVycubAnHnbNFdE2tgI6GUyya6f8&s=10",
        "description": "Leathery, aromatic opposite leaves with dense parallel venation from Girls Hostel lawn.",
    },
    {
        "id": 3,
        "species_id": 3,
        "name": "Jackfruit Leaf (Artocarpus heterophyllus)",
        "scientific_name": "Artocarpus heterophyllus",
        "family": "Moraceae",
        "image_url": "https://m.media-amazon.com/images/I/61uRrl9kpML._AC_UF1000,1000_QL80_.jpg",
        "description": "Stiff, glossy dark-green obovate leaf with prominent central midrib from Boys Hostel courtyard.",
    },
    {
        "id": 4,
        "species_id": 4,
        "name": "False Ashoka Leaf (Polyalthia longifolia)",
        "scientific_name": "Polyalthia longifolia",
        "family": "Annonaceae",
        "image_url": "https://www.tanarata.net/wp-content/uploads/2025/02/False-ashoka-tree-1-1024x682.jpg",
        "description": "Narrow lanceolate leaf with characteristic undulating wavy margins from Main Portico avenue.",
    },
]

CAMPUS_ZONES = [
    "Admin Block & Quadrangle",
    "CSBS & EC Department Enclave",
    "Mechanical & Workshop Avenue",
    "Civil & Environmental Block",
    "Student Hostel & Sports Ground",
    "Main Gate & Perimeter Fence",
]

RESEARCH = {
    "title": "AI BASED FLORA IDENTIFICATION AND BIODIVERSITY MAPPING SYSTEM FOR MCE CAMPUS",
    "app_name": "CampusLeaf",
    "institution": "Malnad College of Engineering, Hassan",
    "institution_details": "An Autonomous Institution under VTU, Belagavi",
    "location": "Hassan, Karnataka – 573201, India",
    "department": "Department of Computer Science and Business Systems (CSBS)",
    "guide": {
        "name": "Dr. Hemanth T S",
        "role": "Project Guide & Associate Professor",
        "department": "Department of CSBS, Malnad College of Engineering, Hassan",
    },
    "authors": [
        {"name": "Dr. Hemanth T S", "role": "Project Guide"},
        {"name": "Samarth H Bharadwaj", "role": "Student Researcher (CSBS)"},
        {"name": "Avinash Subhas Gundanavar", "role": "Student Researcher (CSBS)"},
        {"name": "Abdur Rahman", "role": "Student Researcher (CSBS)"},
        {"name": "Sushanth Gowda S", "role": "Student Researcher (CSBS)"},
        {"name": "Poornachandra P B", "role": "Student Researcher (CSBS)"},
    ],
    "metrics": [
        {"label": "Top-1 Accuracy", "value": "96.4%", "sub": "Rank-1 Match", "tone": "green"},
        {"label": "Top-3 Accuracy", "value": "99.5%", "sub": "Top-3 Window", "tone": "green"},
        {"label": "Macro Precision", "value": "96.1%", "sub": "Across 4 Classes", "tone": "plain"},
        {"label": "Macro Recall", "value": "96.2%", "sub": "True Positive Rate", "tone": "plain"},
        {"label": "Macro F1-Score", "value": "96.1%", "sub": "Harmonic Mean", "tone": "plain"},
        {"label": "Usability (SUS)", "value": "84.2 / 100", "sub": "Excellent Band", "tone": "amber"},
    ],
    "comparison": [
        {"feature": "Target Taxonomy", "ours": "Curated 4 MCE Species (1,000+ Images)", "a": "Global (20,000+ species)", "b": "Global Crowdsourced"},
        {"feature": "Local Kannada Names", "ours": "Native Vernacular Included", "a": "Absent", "b": "Rare / Inconsistent"},
        {"feature": "Campus-Specific GPS Mapping", "ours": "Exact MCE Campus Tree Pins & Zones", "a": "No campus zoning", "b": "Broad regional map"},
        {"feature": "Inference Latency", "ours": "0.28s CPU / Real-time Edge", "a": "1.5s – 3.2s (Cloud API)", "b": "2.0s – 4.0s (Cloud API)"},
        {"feature": "MCE Specific Accuracy", "ours": "96.4% Top-1 (Domain-Adapted)", "a": "~72.4% (General Asian flora)", "b": "~76.1% (General Asian flora)"},
    ],
    "phases": [
        {"title": "Phase 1: Feature Extraction (10 Epochs)", "body": "Base MobileNetV2 layers are frozen with pre-trained ImageNet-1K weights. Only the custom 4-class classification head (GlobalAveragePooling2D, Dropout 0.3, Dense 4 Softmax) is trained using Adam optimizer with initial learning rate 1e-3."},
        {"title": "Phase 2: Fine-Tuning (20 Epochs)", "body": "Top 30 convolution layers of MobileNetV2 are unfrozen. The entire head and top layers are fine-tuned with a reduced learning rate 1e-4 using Cosine Decay schedule and categorical cross-entropy loss with early stopping (patience=5)."},
    ],
    "roadmap": [
        {"title": "1. QR Code Tree Plaques", "body": "Mounting physical weatherproof QR plaques on campus trees linking directly to CampusLeaf digital taxonomy."},
        {"title": "2. Seasonal Phenology Tracker", "body": "Tracking leaf shedding, flowering schedules, and fruit maturation timelines across MCE campus seasons."},
        {"title": "3. Leaf Pathology & Health", "body": "Extending the CNN classifier with a secondary disease detection head for pest and fungal infection triage."},
    ],
}

HERO_IMAGE_URL = "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&auto=format&fit=crop&q=80"

HERO_METRICS = [
    {"value": "4", "label": "Target Species"},
    {"value": "1,000+", "label": "Trained Images"},
    {"value": "96.4%", "label": "Top-1 Accuracy"},
    {"value": "0.28s", "label": "CPU Latency"},
]

WORKFLOW_STEPS = [
    {"n": "01", "title": "Image Acquisition", "body": "Capture via smartphone camera or upload gallery leaf image. Client-side JPEG compression reduces payload to ~280 KB."},
    {"n": "02", "title": "Preprocessing Pipeline", "body": "Aspect-ratio resize to 256×256 px, center-crop to 224×224 px, and MobileNetV2 normalization [-1, +1]."},
    {"n": "03", "title": "MobileNetV2 Inference", "body": "Fine-tuned CNN evaluates the 4 trained campus tree classes, outputting a softmax posterior probability vector with Top-K filtering at τ ≥ 0.30."},
    {"n": "04", "title": "Geospatial Mapping", "body": "Retrieves botanical taxonomy and pins identified specimen on the interactive Leaflet.js MCE campus map."},
]
