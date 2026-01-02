import logging
import cv2
import numpy as np
from deepface import DeepFace
from app.config import Config

logger = logging.getLogger(__name__)

class DeepFaceService:
    @staticmethod
    def detect_and_analyze(image_file):
        """
        Process the image file:
        1. Read image bytes
        2. Decode to opencv format
        3. Detect faces and analyze attributes
        
        Returns:
            list of dicts: Analysis results for each face
        Raises:
            ValueError: If no face detected (and enforcement is on/off handled by caller logic usually, 
                       but deepface throws errors depending on config)
        """
        try:
            # Convert FileStorage to numpy array
            # DeepFace expects a path or a numpy array (BGR)
            npimg = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Could not decode image")

            # DeepFace.analyze calls detection internally.
            # We use extract_faces for just detection, but analyze does both.
            # To be efficient and get both attributes and bbox, we just use analyze.
            # actions=['age', 'emotion']
            # detector_backend=Config.DETECTOR_BACKEND
            
            # NOTE: DeepFace.analyze returns a list of dicts.
            # If enforce_detection=True (default), it raises ValueError if no face found.
            # If enforce_detection=False, it might return dummy data or region 0,0,0,0 depending on version.
            # We stick to Config.ENFORCE_DETECTION passed to valid args.
            
            logger.info(f"Processing image with backend {Config.DETECTOR_BACKEND}")
            
            results = DeepFace.analyze(
                img_path=img,
                actions=['age'], # Removed 'emotion' for performance
                detector_backend=Config.DETECTOR_BACKEND,
                enforce_detection=Config.ENFORCE_DETECTION,
                silent=True # suppress logging
            )
            
            # Normalize results
            # DeepFace >= 0.0.79 returns a list of objects
            # Each obj: {'age': x, 'region': {'x':, 'y':..}, 'emotion': {..}, 'dominant_emotion': ..}
            
            formatted_faces = []
            for face in results:
                # Region is dict {'x': 1, 'y': 1, 'w': 1, 'h': 1}
                region = face.get('region', {})
                
                # Cleanup bbox to ensure standard keys if any variation
                bbox = {
                    "x": region.get('x', 0),
                    "y": region.get('y', 0),
                    "w": region.get('w', 0),
                    "h": region.get('h', 0)
                }
                
                formatted_faces.append({
                    "bbox": bbox,
                    "age": face.get('age'),
                    # "dominant_emotion": face.get('dominant_emotion'), # Removed
                    # "emotion": face.get('emotion'), # Removed
                    "confidence": face.get('face_confidence', None) # Available in some backends/versions
                })
                
            return formatted_faces

        except ValueError as e:
            # DeepFace raises ValueError when Face could not be detected and enforce_detection is True
            logger.warning(f"DeepFace processing error (likely no face): {str(e)}")
            raise ValueError("No face detected")
        except Exception as e:
            logger.error(f"Unexpected error in deepface service: {str(e)}")
            raise e
