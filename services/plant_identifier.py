import time
import random
from typing import Optional, Dict, Any
from models.plant import PlantPrediction

def identify_plant(image) -> Optional[Dict[str, Any]]:
    """
    Mock ML identification service.
    In the future, this will receive an image and call an actual ML model
    or external API to identify the plant.
    """
    # Simulate processing time
    time.sleep(2.5)

    # We mock returning a Mango prediction.
    # In a real scenario, this would depend on the image.
    
    # Randomly simulate an error for robustness testing (rarely)
    # if random.random() < 0.05:
    #     raise ConnectionError("Could not reach ML service")

    return {
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "confidence": 0.94,
        "family": "Anacardiaceae",
        "description": "A tropical evergreen tree with long, glossy leaves and edible fruit.",
        "uses": [
            "Fruit",
            "Shade",
            "Ornamental"
        ]
    }
