# Campus Plant ID 🌿

**Campus Plant ID** is a Streamlit-based digital herbarium that identifies selected plant species from photographs and checks whether the identified species exists in the campus plant catalog.

The application combines a locally running MobileNetV2 image-classification model, a Supabase PostgreSQL database, and a botanical herbarium-inspired interface.

## ✨ Features

- **Local plant identification:** Predicts plant species using a trained MobileNetV2 model without external plant-identification APIs.
- **Four supported species:** Identifies False Ashoka, Jackfruit, Malabar Plum, and Pongam.
- **Supabase integration:** Retrieves plant information and campus catalog records from Supabase.
- **Confidence scores:** Displays the model's prediction confidence.
- **Specimen cards:** Presents botanical information through a herbarium-inspired interface.
- **Catalog status:** Distinguishes plants found in the campus database from identified plants that are not catalogued.
- **Responsive interface:** Designed for students to use while exploring the campus.

## 🌱 Supported Plant Species

| Common Name | Scientific Name | Family |
|---|---|---|
| False Ashoka | *Monoon longifolium* | Annonaceae |
| Jackfruit | *Artocarpus heterophyllus* | Moraceae |
| Malabar Plum | *Syzygium cumini* | Myrtaceae |
| Pongam | *Pongamia pinnata* | Fabaceae |

The classifier is trained to recognize these four classes. It is not a general-purpose plant identification system.

## 🧠 Machine Learning Model

The application uses a locally stored MobileNetV2 transfer-learning model.

- **Architecture:** MobileNetV2
- **Framework:** TensorFlow / Keras
- **Model file:** `models/campus_plant_id_mobilenetv2.keras`
- **Input image size:** 224 × 224 pixels
- **Inference:** Local model execution
- **Output:** Predicted species and confidence score

The reported evaluation achieved **98.82% accuracy (84 correct predictions out of 85 test images)**.

This is a preliminary result from a relatively small test set. Performance on unseen campus photographs, different lighting conditions, backgrounds, and camera devices requires further evaluation. The confidence score should not be interpreted as a guarantee of identification correctness.

### Identification Workflow

1. The user uploads a plant photograph.
2. The image is preprocessed for the local model.
3. MobileNetV2 predicts one of the supported species.
4. The application retrieves the corresponding plant information from Supabase.
5. The interface displays the specimen card or an appropriate catalog/error state.

```text
Plant Photograph
       |
       v
Image Preprocessing
       |
       v
Local MobileNetV2 Model
       |
       v
Predicted Species + Confidence
       |
       v
Supabase Catalog Lookup
       |
       +----------------------+
       |                      |
       v                      v
Plant Record Found      Record Not Found
       |                      |
       v                      v
Specimen Card           Not Catalogued State
```

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| Machine Learning | TensorFlow / Keras |
| Model Architecture | MobileNetV2 |
| Image Processing | Pillow |
| Database | Supabase PostgreSQL |
| Database Client | Supabase Python Client |
| Configuration | python-dotenv |

## 📂 Project Structure

The main application components are organized as follows:

```text
campusLeaf/
├── app.py
├── services/
│   ├── plant_identifier.py
│   └── campus_repository.py
├── models/
│   ├── plant.py
│   └── campus_plant_id_mobilenetv2.keras
├── ui/
│   ├── identification.py
│   ├── specimen_card.py
│   └── styles.py
├── requirements.txt
├── .env.example
└── README.md
```

This is a representative overview of the main components. Additional files, assets, and tests may exist in the repository.

## ⚙️ Installation and Setup

### Prerequisites

- Python compatible with the versions specified in `requirements.txt`
- Git
- A configured Supabase project
- Access to the project's model file and source code

### 1. Clone the Repository

```bash
git clone <repository-url>
cd campusLeaf
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Create a Virtual Environment

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Keep TensorFlow and NumPy versions compatible with those specified in the project's dependency configuration.

### 4. Configure Supabase

Create a `.env` file in the project root using `.env.example` as a reference.

Example:

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-key
```

Replace the example values with the credentials expected by the current application configuration.

Ensure that the Supabase project contains the required tables, records, and access policies.

**Security notes:**
- Never commit `.env` to GitHub.
- Never expose Supabase service-role keys in public code.
- Use appropriate Row Level Security (RLS) policies and least-privilege access.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## 🧪 Testing

Run the existing Supabase integration tests from the project root:

```bash
python -m pytest test_supabase_integration.py test_supabase_pipeline.py
```

If the project uses additional test configuration, follow the repository's current setup.

Recommended manual checks:

1. Upload photographs from all four supported species.
2. Verify the predicted species and confidence score.
3. Verify the result when a corresponding Supabase record exists.
4. Verify the not-catalogued state when no matching record exists.
5. Verify that database errors are not incorrectly displayed as missing records.
6. Test unsupported images, corrupt files, and low-confidence predictions.
7. Check the interface on both desktop and mobile-sized screens.

## 🗄️ Database Integration

Supabase serves as the application's campus plant catalog.

The machine-learning model and database have separate responsibilities:

- The **ML model** predicts a likely plant species from the uploaded image.
- **Supabase** stores and retrieves catalog information associated with that species.
- The **Streamlit interface** presents the identification result and catalog status.

A successful prediction does not necessarily mean the plant has been documented on campus. Similarly, a missing database record does not automatically mean the ML prediction failed.

Catalog records, scientific names, and campus locations should be verified rather than fabricated.

## 🔒 External API Policy

Campus Plant ID performs plant identification locally using its trained model.

- No external plant-identification API is required.
- No API-based prediction validation is used.
- No external identification service is used as a runtime fallback.
- No third-party API key is needed for plant identification.

External image datasets may be considered for future local model training or evaluation, subject to appropriate licensing and data-quality checks. Using a dataset does not require calling an external identification API at runtime.

## 🚧 Limitations

- The current classifier recognizes only four trained plant species.
- Unfamiliar plants may be incorrectly assigned to one of the supported classes.
- Model confidence is not proof of correctness.
- The reported test accuracy comes from a small test set.
- Identification accuracy depends on image quality and similarity to the training data.
- Campus location information depends on the completeness and accuracy of database records.
- Further evaluation using independent campus photographs is recommended before relying on the system operationally.

## 🔮 Future Improvements

Potential improvements include:

- Expanding the supported campus plant collection.
- Collecting more diverse, verified training images.
- Evaluating the model on independent photographs from the campus.
- Reporting per-class precision, recall, F1-score, and a confusion matrix.
- Improving handling of unknown species and low-confidence predictions.
- Adding verified campus locations and additional botanical information.
- Improving accessibility and mobile usability.

Any replacement model should be evaluated before being adopted, and the existing Supabase integration and interface should be preserved unless a change is explicitly required.

## 📄 License

Add the project's chosen license before publishing or redistributing the repository.
