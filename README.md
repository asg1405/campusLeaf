# Campus Plant ID — Phase 2: Supabase Integration

Campus Plant ID is a digital herbarium application for discovering, identifying, and locating botanical specimens across campus.

---

## 🏗️ Architecture & Integration Points

The application is structured into decoupled layers, ensuring that the machine learning service, backend database, and user interface remain modular and interchangeable:

```text
User
 ↓
Streamlit UI (Design 2 Aesthetic)
 ↓
Image Upload / Camera
 ↓
Plant Identifier Service (Mock ML — Phase 3 target)
 ↓
Campus Repository Service (Abstraction Boundary)
 ↓
Supabase PostgreSQL Database (Phase 2 Integration)
 ↓
Digital Specimen Card
```

- **`app.py`**: State orchestrator managing the workflow (`IDLE` $\rightarrow$ `IMAGE_SELECTED` $\rightarrow$ `IDENTIFYING` $\rightarrow$ `FOUND` / `NOT_CATALOGUED` / `ERROR`).
- **`services/plant_identifier.py`**: Exposes `identify_plant(image)`. Currently runs mock ML predictions.
  > *Note: The ML identification service is currently mocked and will be replaced by the real plant classification model in Phase 3.*
- **`services/campus_repository.py`**: Exposes `campus_lookup(scientific_name)` to query the database.
- **`services/supabase_client.py`**: Safely retrieves configuration and initializes the official Supabase client.
- **`models/plant.py`**: Application data models (`PlantPrediction`, `CampusPlantRecord`, `CampusLocation`).
- **`ui/`**: Herbarium field-journal visual components (Design 2), custom typography, scan radar animations, and specimen cards.

---

## 🗄️ Database Schema

The Supabase relational schema consists of:

### `plants` Table
- `id` (UUID, Primary Key, auto-generated)
- `common_name` (TEXT, NOT NULL)
- `scientific_name` (TEXT, UNIQUE, NOT NULL, indexed with `LOWER(scientific_name)`)
- `family` (TEXT, NOT NULL)
- `description` (TEXT)
- `uses` (TEXT[])
- `facts` (TEXT[])
- `image_url` (TEXT, ready for Supabase Storage in future phases)
- `created_at` (TIMESTAMPTZ)
- `updated_at` (TIMESTAMPTZ)

### `campus_locations` Table (One-to-Many)
- `id` (UUID, Primary Key, auto-generated)
- `plant_id` (UUID, Foreign Key $\rightarrow$ `plants.id`, ON DELETE CASCADE, indexed)
- `location_name` (TEXT, NOT NULL)
- `latitude` (NUMERIC, optional)
- `longitude` (NUMERIC, optional)
- `description` (TEXT, optional)
- `created_at` (TIMESTAMPTZ)

---

## 🚀 Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create and Configure Supabase Project
1. Log in to [Supabase](https://supabase.com) and create a new project.
2. In the Supabase dashboard, open the **SQL Editor**.
3. Copy the contents of [`scripts/setup_supabase.sql`](file:///c:/github/avinashProject/campus-plant-id/scripts/setup_supabase.sql) into the editor and click **Run** to generate tables, indexes, and RLS policies.

### 3. Configure Credentials
Create a `.env` file in the `campus-plant-id` folder (or configure Streamlit secrets in `.streamlit/secrets.toml`):

```bash
cp .env.example .env
```

Edit `.env` and fill in your Supabase project credentials:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_or_anon_key
```

> **Security Note:** Use your project's **publishable / anon** API key. Do **NOT** use or configure the `service_role` key in the Streamlit application. The `service_role` key bypasses Row Level Security (RLS) with elevated administrative privileges and must never be exposed or bundled in client-facing applications.

*(Never commit your `.env` or `.streamlit/secrets.toml` file. These are protected in `.gitignore`.)*

### 4. Seed Campus Plant Demo Data
To populate your Supabase database with the initial campus flora dataset:
```bash
python scripts/seed_demo_data.py
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🧪 Application States

- **`READY / IDLE`**: Drag & drop a plant photo or use camera capture.
- **`IDENTIFYING`**: Visual scan-line radar animation simulating ML processing.
- **`FOUND`**: Specimen found in campus botanical records. Displays specimen card with locations, uses, and facts.
- **`NOT_CATALOGUED`**: Plant is identified by the ML service, but is not yet recorded in the campus flora registry.
- **`ERROR`**: Graceful service notice for network issues or unconfigured credentials with instant retry.
