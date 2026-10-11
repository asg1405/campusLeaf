
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Any
import logging

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError


logger = logging.getLogger(__name__)

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "campus_plant_id_mobilenetv2.keras"
)

IMAGE_SIZE = (224, 224)
MIN_CONFIDENCE = 0.60

# Must match the exact class order used during training.
PLANT_CLASSES = {
    "false_ashoka": {
        "common_name": "False Ashoka",
        "scientific_name": "Monoon longifolium",
        "family": "Annonaceae",
        "description": (
            "An evergreen ornamental tree commonly planted "
            "along campus pathways and boundaries."
        ),
        "uses": ["Ornamental", "Shade", "Landscaping"],
    },
    "jackfruit": {
        "common_name": "Jackfruit",
        "scientific_name": "Artocarpus heterophyllus",
        "family": "Moraceae",
        "description": (
            "A tropical evergreen tree known for producing "
            "large edible fruits."
        ),
        "uses": ["Food", "Timber", "Shade"],
    },
    "malbar_plum": {
        "common_name": "Malabar Plum",
        "scientific_name": "Syzygium cumini",
        "family": "Myrtaceae",
        "description": (
            "An evergreen tree commonly known for its "
            "purple-black edible fruits."
        ),
        "uses": ["Food", "Shade", "Landscaping"],
    },
    "pongam": {
        "common_name": "Pongam",
        "scientific_name": "Pongamia pinnata",
        "family": "Fabaceae",
        "description": (
            "A hardy tree often planted for shade and "
            "landscaping, with traditional uses for its seeds."
        ),
        "uses": ["Shade", "Landscaping", "Traditional uses"],
    },
}


@lru_cache(maxsize=1)
def _load_model():
    """Load the trained model once per application process."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Trained plant model not found: {MODEL_PATH}"
        )

    return tf.keras.models.load_model(
        MODEL_PATH,
        compile=False,
    )


def identify_plant(image) -> Optional[Dict[str, Any]]:
    """
    Identify one of the four supported campus plant species.

    Accepts a PIL image or a file-like image object.
    Returns the existing prediction dictionary format.
    """
    try:
        if isinstance(image, Image.Image):
            pil_image = image
        else:
            # Supports Streamlit UploadedFile and similar objects.
            if hasattr(image, "seek"):
                image.seek(0)

            pil_image = Image.open(image)

        pil_image = pil_image.convert("RGB")
        pil_image = pil_image.resize(
            IMAGE_SIZE,
            Image.Resampling.LANCZOS,
        )

        # The trained model contains MobileNetV2 preprocessing.
        # Pass RGB pixel values in the 0–255 range.
        image_array = np.asarray(
            pil_image,
            dtype=np.float32,
        )
        image_batch = np.expand_dims(image_array, axis=0)

        model = _load_model()
        probabilities = model.predict(image_batch, verbose=0)[0]

        if len(probabilities) != len(PLANT_CLASSES):
            raise ValueError(
                "Model output count does not match the four "
                "configured plant classes."
            )

        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index])

        class_name = list(PLANT_CLASSES.keys())[predicted_index]

        # Avoid presenting low-confidence predictions as certain.
        if confidence < MIN_CONFIDENCE:
            return None

        plant_info = PLANT_CLASSES[class_name]

        return {
            **plant_info,
            "confidence": confidence,
        }

    except (UnidentifiedImageError, OSError, ValueError, AttributeError, TypeError) as e:
        # Invalid image input (including None) or malformed model output.
        logger.debug("Plant identification failed for invalid input: %s", type(e).__name__)
        return None
