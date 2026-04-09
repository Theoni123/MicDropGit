"""
Video processing utilities for body language analysis
Uses MediaPipe Tasks API for pose, face, and hand detection
(Python 3.13+ wheels no longer expose the legacy mp.solutions API.)
"""

import cv2
import numpy as np
import mediapipe as mp
import tempfile
import os
from pathlib import Path
from urllib.request import urlretrieve
from typing import Dict, List, Tuple, Optional
import math

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

_MEDIAPIPE_TASK_MODELS = {
    "pose_landmarker_lite.task": (
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
        "pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    ),
    "face_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
        "face_landmarker/float16/1/face_landmarker.task"
    ),
    "hand_landmarker.task": (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/hand_landmarker.task"
    ),
}


def _mediapipe_model_cache_dir() -> Path:
    env = os.environ.get("MICDROP_MEDIAPIPE_CACHE")
    if env:
        return Path(env)
    return Path.home() / ".cache" / "micdrop_mediapipe"


def _ensure_task_model(filename: str) -> str:
    cache = _mediapipe_model_cache_dir()
    cache.mkdir(parents=True, exist_ok=True)
    dest = cache / filename
    if dest.is_file():
        return str(dest)
    url = _MEDIAPIPE_TASK_MODELS.get(filename)
    if not url:
        raise FileNotFoundError(f"No bundled download URL for MediaPipe model {filename!r}")
    part = dest.with_suffix(dest.suffix + ".part")
    try:
        urlretrieve(url, part)
        part.replace(dest)
    except Exception:
        if part.is_file():
            part.unlink(missing_ok=True)
        raise
    return str(dest)


class _NormalizedLandmarkView:
    __slots__ = ("x", "y", "z")

    def __init__(self, lm):
        self.x = float(lm.x) if lm.x is not None else 0.0
        self.y = float(lm.y) if lm.y is not None else 0.0
        self.z = float(lm.z) if lm.z is not None else 0.0


class _LandmarksAsSolution:
    """Mimics solutions.* `.landmark[i].x` access for downstream analyzers."""

    __slots__ = ("landmark",)

    def __init__(self, normalized_list):
        self.landmark = [_NormalizedLandmarkView(lm) for lm in normalized_list]


def _bgr_frame_to_mp_image(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = np.ascontiguousarray(rgb)
    return mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

# Try to import streamlit for caching (optional)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None


def load_video(video_file, max_frames: Optional[int] = None):
    """
    Load video file and extract frames
    
    Args:
        video_file: Uploaded file or file path
        max_frames: Maximum number of frames to process (None = all)
    
    Returns:
        frames: List of frame arrays (BGR format)
        fps: Frames per second
        total_frames: Total number of frames
    """
    tmp_path = None
    try:
        # Handle Streamlit uploaded file
        if hasattr(video_file, 'read'):
            # Save to temporary file
            video_bytes = video_file.read()
            video_file.seek(0)  # Reset file pointer
            
            # Get file extension
            file_ext = os.path.splitext(video_file.name)[1] if hasattr(video_file, 'name') else '.mp4'
            if not file_ext:
                file_ext = '.mp4'
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                tmp_file.write(video_bytes)
                tmp_path = tmp_file.name
        else:
            tmp_path = video_file
        
        # Open video with OpenCV
        cap = cv2.VideoCapture(tmp_path)
        
        if not cap.isOpened():
            raise Exception("Could not open video file")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample frames (every 0.5 seconds for efficiency)
        frame_interval = max(1, int(fps * 0.5))  # Sample every 0.5 seconds
        
        frames = []
        frame_numbers = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames at intervals
            if frame_count % frame_interval == 0:
                frames.append(frame)
                frame_numbers.append(frame_count)
                
                if max_frames and len(frames) >= max_frames:
                    break
            
            frame_count += 1
        
        cap.release()
        
        return frames, fps, total_frames, frame_numbers
        
    except Exception as e:
        raise Exception(f"Error loading video: {str(e)}")
    finally:
        # Clean up temp file
        if tmp_path and hasattr(video_file, 'read') and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass


def _build_mediapipe_landmarkers():
    pose_path = _ensure_task_model("pose_landmarker_lite.task")
    face_path = _ensure_task_model("face_landmarker.task")
    hand_path = _ensure_task_model("hand_landmarker.task")

    pose_options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=pose_path),
        running_mode=VisionRunningMode.IMAGE,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    face_options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=face_path),
        running_mode=VisionRunningMode.IMAGE,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=hand_path),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    return {
        "pose": PoseLandmarker.create_from_options(pose_options),
        "face_mesh": FaceLandmarker.create_from_options(face_options),
        "hands": HandLandmarker.create_from_options(hand_options),
    }


# Cache MediaPipe models if streamlit is available
if HAS_STREAMLIT:
    @st.cache_resource
    def get_mediapipe_models():
        """Get MediaPipe Tasks landmarkers with caching (downloads .task models once)."""
        return _build_mediapipe_landmarkers()
else:
    def get_mediapipe_models():
        """Get MediaPipe Tasks landmarkers without caching."""
        return _build_mediapipe_landmarkers()


def detect_pose_landmarks(frame, pose_model):
    """
    Detect pose landmarks in a frame
    
    Args:
        frame: BGR image frame
        pose_model: MediaPipe PoseLandmarker
    
    Returns:
        landmarks: Pose landmarks or None
    """
    mp_image = _bgr_frame_to_mp_image(frame)
    result = pose_model.detect(mp_image)
    if result.pose_landmarks and len(result.pose_landmarks) > 0:
        return _LandmarksAsSolution(result.pose_landmarks[0])
    return None


def detect_face_landmarks(frame, face_model):
    """
    Detect face landmarks in a frame
    
    Args:
        frame: BGR image frame
        face_model: MediaPipe FaceLandmarker
    
    Returns:
        landmarks: Face landmarks or None
    """
    mp_image = _bgr_frame_to_mp_image(frame)
    result = face_model.detect(mp_image)
    if result.face_landmarks and len(result.face_landmarks) > 0:
        return _LandmarksAsSolution(result.face_landmarks[0])
    return None


def detect_hand_landmarks(frame, hands_model):
    """
    Detect hand landmarks in a frame
    
    Args:
        frame: BGR image frame
        hands_model: MediaPipe HandLandmarker
    
    Returns:
        landmarks: List of hand landmarks (up to 2 hands)
    """
    mp_image = _bgr_frame_to_mp_image(frame)
    result = hands_model.detect(mp_image)
    if result.hand_landmarks:
        return [_LandmarksAsSolution(h) for h in result.hand_landmarks]
    return []


def calculate_angle(point1, point2, point3):
    """
    Calculate angle between three points
    
    Args:
        point1, point2, point3: (x, y) tuples
    
    Returns:
        angle: Angle in degrees
    """
    # Vector from point2 to point1
    v1 = (point1[0] - point2[0], point1[1] - point2[1])
    # Vector from point2 to point3
    v2 = (point3[0] - point2[0], point3[1] - point2[1])
    
    # Calculate angle
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    cos_angle = dot_product / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
    angle = math.degrees(math.acos(cos_angle))
    
    return angle


def analyze_posture(pose_landmarks_list, frame_width, frame_height):
    """
    Analyze posture from pose landmarks
    
    Args:
        pose_landmarks_list: List of pose landmarks across frames
        frame_width: Frame width
        frame_height: Frame height
    
    Returns:
        Dictionary with posture metrics
    """
    if not pose_landmarks_list:
        return {
            'posture_score': 0.0,
            'shoulder_alignment': 0.0,
            'spine_alignment': 0.0,
            'slouching_detected': True,
            'upright_percentage': 0.0
        }
    
    # MediaPipe pose landmark indices
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    NOSE = 0
    
    shoulder_alignments = []
    spine_angles = []
    upright_count = 0
    
    for landmarks in pose_landmarks_list:
        if not landmarks:
            continue
        
        # Get landmark positions
        left_shoulder = landmarks.landmark[LEFT_SHOULDER]
        right_shoulder = landmarks.landmark[RIGHT_SHOULDER]
        left_hip = landmarks.landmark[LEFT_HIP]
        right_hip = landmarks.landmark[RIGHT_HIP]
        nose = landmarks.landmark[NOSE]
        
        # Calculate shoulder alignment (horizontal difference)
        shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
        shoulder_alignments.append(shoulder_diff)
        
        # Calculate spine angle (angle between shoulders and hips)
        shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_mid_x = (left_hip.x + right_hip.x) / 2
        hip_mid_y = (left_hip.y + right_hip.y) / 2
        
        # Calculate angle from vertical (0 = perfectly upright)
        spine_angle = math.degrees(math.atan2(
            hip_mid_x - shoulder_mid_x,
            hip_mid_y - shoulder_mid_y
        ))
        spine_angles.append(abs(spine_angle))
        
        # Determine if upright (spine angle < 15 degrees, shoulders aligned)
        if abs(spine_angle) < 15 and shoulder_diff < 0.05:
            upright_count += 1
    
    # Calculate averages
    avg_shoulder_alignment = np.mean(shoulder_alignments) if shoulder_alignments else 1.0
    avg_spine_angle = np.mean(spine_angles) if spine_angles else 90.0
    upright_percentage = upright_count / len(pose_landmarks_list) if pose_landmarks_list else 0.0
    
    # Posture score (0-1, higher is better)
    # Good posture: spine angle < 15°, shoulder alignment < 0.05
    spine_score = max(0, 1 - (avg_spine_angle / 45))  # 0° = 1.0, 45° = 0.0
    shoulder_score = max(0, 1 - (avg_shoulder_alignment / 0.1))  # 0 = 1.0, 0.1 = 0.0
    posture_score = (spine_score * 0.6 + shoulder_score * 0.4)
    
    # Detect slouching (spine angle > 20° or shoulders misaligned > 0.08)
    slouching_detected = avg_spine_angle > 20 or avg_shoulder_alignment > 0.08
    
    return {
        'posture_score': posture_score,
        'shoulder_alignment': avg_shoulder_alignment,
        'spine_alignment': avg_spine_angle,
        'slouching_detected': slouching_detected,
        'upright_percentage': upright_percentage
    }


def analyze_gestures(hand_landmarks_list):
    """
    Analyze hand gestures and movements
    
    Args:
        hand_landmarks_list: List of hand landmarks across frames
    
    Returns:
        Dictionary with gesture metrics
    """
    if not hand_landmarks_list:
        return {
            'gesture_count': 0,
            'hand_movement_score': 0.0,
            'gesture_frequency': 0.0,
            'hands_visible_percentage': 0.0
        }
    
    # Count frames with hands visible
    hands_visible = sum(1 for hands in hand_landmarks_list if hands)
    hands_visible_percentage = hands_visible / len(hand_landmarks_list) if hand_landmarks_list else 0.0
    
    # Track hand positions over time to detect movement
    hand_positions = []
    gesture_count = 0
    
    for hands in hand_landmarks_list:
        if not hands:
            continue
        
        for hand_landmarks in hands:
            # Get wrist position (landmark 0)
            wrist = hand_landmarks.landmark[0]
            hand_positions.append((wrist.x, wrist.y))
    
    # Calculate movement (distance between consecutive positions)
    if len(hand_positions) > 1:
        movements = []
        for i in range(1, len(hand_positions)):
            dx = hand_positions[i][0] - hand_positions[i-1][0]
            dy = hand_positions[i][1] - hand_positions[i-1][1]
            distance = math.sqrt(dx**2 + dy**2)
            movements.append(distance)
            
            # Count gestures (significant movements > threshold)
            if distance > 0.02:  # Threshold for gesture detection
                gesture_count += 1
        
        avg_movement = np.mean(movements) if movements else 0.0
        hand_movement_score = min(1.0, avg_movement * 50)  # Normalize to 0-1
    else:
        hand_movement_score = 0.0
    
    # Calculate gesture frequency (gestures per second, approximate)
    # Assuming ~2 frames per second (sampling every 0.5s)
    gesture_frequency = gesture_count / (len(hand_landmarks_list) * 0.5) if hand_landmarks_list else 0.0
    
    return {
        'gesture_count': gesture_count,
        'hand_movement_score': hand_movement_score,
        'gesture_frequency': gesture_frequency,
        'hands_visible_percentage': hands_visible_percentage
    }


def analyze_eye_contact(face_landmarks_list, frame_width, frame_height):
    """
    Analyze eye contact (gaze direction)
    
    Args:
        face_landmarks_list: List of face landmarks across frames
        frame_width: Frame width
        frame_height: Frame height
    
    Returns:
        Dictionary with eye contact metrics
    """
    if not face_landmarks_list:
        return {
            'eye_contact_percentage': 0.0,
            'gaze_direction': 'unknown',
            'face_visible_percentage': 0.0
        }
    
    # MediaPipe face mesh indices for eyes
    LEFT_EYE_TOP = 159
    LEFT_EYE_BOTTOM = 145
    RIGHT_EYE_TOP = 386
    RIGHT_EYE_BOTTOM = 374
    NOSE_TIP = 1
    
    eye_contact_count = 0
    gaze_directions = []
    
    for landmarks in face_landmarks_list:
        if not landmarks:
            continue
        
        # Get eye positions
        left_eye_top = landmarks.landmark[LEFT_EYE_TOP]
        left_eye_bottom = landmarks.landmark[LEFT_EYE_BOTTOM]
        right_eye_top = landmarks.landmark[RIGHT_EYE_TOP]
        right_eye_bottom = landmarks.landmark[RIGHT_EYE_BOTTOM]
        nose_tip = landmarks.landmark[NOSE_TIP]
        
        # Calculate eye centers
        left_eye_center_y = (left_eye_top.y + left_eye_bottom.y) / 2
        right_eye_center_y = (right_eye_top.y + right_eye_bottom.y) / 2
        
        # Estimate gaze direction based on nose position relative to eyes
        # If nose is centered and eyes are level, likely looking at camera
        eye_level = (left_eye_center_y + right_eye_center_y) / 2
        nose_offset = abs(nose_tip.x - 0.5)  # 0.5 is center of frame
        
        # Simple heuristic: if nose is near center and eyes are level, likely eye contact
        if nose_offset < 0.1 and abs(left_eye_center_y - right_eye_center_y) < 0.01:
            eye_contact_count += 1
            gaze_directions.append('camera')
        elif nose_tip.x < 0.4:
            gaze_directions.append('left')
        elif nose_tip.x > 0.6:
            gaze_directions.append('right')
        else:
            gaze_directions.append('center')
    
    face_visible_percentage = len(face_landmarks_list) / len(face_landmarks_list) if face_landmarks_list else 0.0
    eye_contact_percentage = eye_contact_count / len(face_landmarks_list) if face_landmarks_list else 0.0
    
    # Determine most common gaze direction
    if gaze_directions:
        from collections import Counter
        most_common = Counter(gaze_directions).most_common(1)[0][0]
    else:
        most_common = 'unknown'
    
    return {
        'eye_contact_percentage': eye_contact_percentage,
        'gaze_direction': most_common,
        'face_visible_percentage': face_visible_percentage
    }


def analyze_facial_expressions(face_landmarks_list):
    """
    Analyze facial expressions for engagement and confidence
    
    Args:
        face_landmarks_list: List of face landmarks across frames
    
    Returns:
        Dictionary with facial expression metrics
    """
    if not face_landmarks_list:
        return {
            'smile_percentage': 0.0,
            'engagement_score': 0.0,
            'confidence_score': 0.0
        }
    
    # MediaPipe face mesh indices
    MOUTH_LEFT = 61
    MOUTH_RIGHT = 291
    MOUTH_TOP = 13
    MOUTH_BOTTOM = 14
    LEFT_EYE_TOP = 159
    LEFT_EYE_BOTTOM = 145
    RIGHT_EYE_TOP = 386
    RIGHT_EYE_BOTTOM = 374
    
    smiles = 0
    eye_openness_scores = []
    
    for landmarks in face_landmarks_list:
        if not landmarks:
            continue
        
        # Analyze mouth (smile detection)
        mouth_left = landmarks.landmark[MOUTH_LEFT]
        mouth_right = landmarks.landmark[MOUTH_RIGHT]
        mouth_top = landmarks.landmark[MOUTH_TOP]
        mouth_bottom = landmarks.landmark[MOUTH_BOTTOM]
        
        # Calculate mouth width and height
        mouth_width = abs(mouth_right.x - mouth_left.x)
        mouth_height = abs(mouth_bottom.y - mouth_top.y)
        
        # Smile: wider mouth relative to height
        if mouth_width > mouth_height * 2.5:
            smiles += 1
        
        # Analyze eye openness (engagement indicator)
        left_eye_height = abs(landmarks.landmark[LEFT_EYE_TOP].y - landmarks.landmark[LEFT_EYE_BOTTOM].y)
        right_eye_height = abs(landmarks.landmark[RIGHT_EYE_TOP].y - landmarks.landmark[RIGHT_EYE_BOTTOM].y)
        avg_eye_height = (left_eye_height + right_eye_height) / 2
        eye_openness_scores.append(avg_eye_height)
    
    smile_percentage = smiles / len(face_landmarks_list) if face_landmarks_list else 0.0
    avg_eye_openness = np.mean(eye_openness_scores) if eye_openness_scores else 0.0
    
    # Engagement score: combination of smiles and eye openness
    engagement_score = (smile_percentage * 0.5 + min(1.0, avg_eye_openness * 20) * 0.5)
    
    # Confidence score: based on facial symmetry and openness
    # More open eyes and natural expressions indicate confidence
    confidence_score = min(1.0, avg_eye_openness * 15) * 0.6 + smile_percentage * 0.4
    
    return {
        'smile_percentage': smile_percentage,
        'engagement_score': engagement_score,
        'confidence_score': confidence_score
    }


def analyze_movement(pose_landmarks_list, frame_width, frame_height):
    """
    Analyze body movement (stationary vs excessive movement)
    
    Args:
        pose_landmarks_list: List of pose landmarks across frames
        frame_width: Frame width
        frame_height: Frame height
    
    Returns:
        Dictionary with movement metrics
    """
    if not pose_landmarks_list or len(pose_landmarks_list) < 2:
        return {
            'movement_score': 0.0,
            'movement_type': 'stationary',
            'body_center_positions': []
        }
    
    # Track body center (midpoint between hips) over time
    LEFT_HIP = 23
    RIGHT_HIP = 24
    
    body_centers = []
    
    for landmarks in pose_landmarks_list:
        if not landmarks:
            continue
        
        left_hip = landmarks.landmark[LEFT_HIP]
        right_hip = landmarks.landmark[RIGHT_HIP]
        
        center_x = (left_hip.x + right_hip.x) / 2
        center_y = (left_hip.y + right_hip.y) / 2
        body_centers.append((center_x, center_y))
    
    # Calculate movement distances
    if len(body_centers) > 1:
        movements = []
        for i in range(1, len(body_centers)):
            dx = body_centers[i][0] - body_centers[i-1][0]
            dy = body_centers[i][1] - body_centers[i-1][1]
            distance = math.sqrt(dx**2 + dy**2)
            movements.append(distance)
        
        avg_movement = np.mean(movements) if movements else 0.0
        max_movement = max(movements) if movements else 0.0
        
        # Movement score (0-1)
        # Optimal: some movement (0.01-0.03), too much (>0.05) or too little (<0.005) is bad
        if avg_movement < 0.005:
            movement_score = 0.3  # Too stationary
            movement_type = 'stationary'
        elif avg_movement > 0.05:
            movement_score = 0.4  # Too much movement
            movement_type = 'excessive'
        else:
            movement_score = 1.0  # Good movement
            movement_type = 'appropriate'
    else:
        movement_score = 0.0
        movement_type = 'unknown'
        avg_movement = 0.0
    
    return {
        'movement_score': movement_score,
        'movement_type': movement_type,
        'average_movement': avg_movement,
        'body_center_positions': body_centers
    }


def process_video(video_file, max_frames: Optional[int] = 100):
    """
    Process video and extract body language metrics
    
    Args:
        video_file: Uploaded video file or path
        max_frames: Maximum frames to process (for performance)
    
    Returns:
        Dictionary with all body language metrics
    """
    # Load video frames
    frames, fps, total_frames, frame_numbers = load_video(video_file, max_frames)
    
    if not frames:
        raise Exception("No frames extracted from video")
    
    # Get MediaPipe models
    models = get_mediapipe_models()
    
    # Process each frame
    pose_landmarks_list = []
    face_landmarks_list = []
    hand_landmarks_list = []
    
    for frame in frames:
        # Detect pose
        pose_landmarks = detect_pose_landmarks(frame, models['pose'])
        pose_landmarks_list.append(pose_landmarks)
        
        # Detect face
        face_landmarks = detect_face_landmarks(frame, models['face_mesh'])
        face_landmarks_list.append(face_landmarks)
        
        # Detect hands
        hand_landmarks = detect_hand_landmarks(frame, models['hands'])
        hand_landmarks_list.append(hand_landmarks)
    
    # Get frame dimensions
    frame_height, frame_width = frames[0].shape[:2]
    
    # Analyze all metrics
    posture_metrics = analyze_posture(pose_landmarks_list, frame_width, frame_height)
    gesture_metrics = analyze_gestures(hand_landmarks_list)
    eye_contact_metrics = analyze_eye_contact(face_landmarks_list, frame_width, frame_height)
    expression_metrics = analyze_facial_expressions(face_landmarks_list)
    movement_metrics = analyze_movement(pose_landmarks_list, frame_width, frame_height)
    
    # Calculate overall presence score
    presence_score = (
        posture_metrics['posture_score'] * 0.25 +
        min(1.0, gesture_metrics['hand_movement_score'] * 2) * 0.20 +
        eye_contact_metrics['eye_contact_percentage'] * 0.25 +
        expression_metrics['engagement_score'] * 0.15 +
        movement_metrics['movement_score'] * 0.15
    )
    
    return {
        'posture': posture_metrics,
        'gestures': gesture_metrics,
        'eye_contact': eye_contact_metrics,
        'facial_expressions': expression_metrics,
        'movement': movement_metrics,
        'presence_score': presence_score,
        'frames_processed': len(frames),
        'total_frames': total_frames,
        'fps': fps,
        'duration': total_frames / fps if fps > 0 else 0
    }

