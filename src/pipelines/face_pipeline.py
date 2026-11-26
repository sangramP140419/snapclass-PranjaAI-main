import numpy as np
import dlib
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)
    
    encodings = []
    
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        
        encodings.append(np.array(face_descriptor))
        
    return encodings

@st.cache_resource
def get_trained_models():
    X = []
    y = []
    
    student_db = get_all_students()
    
    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))
            
    if len(X) == 0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    
    try:
        clf.fit(X, y)
    except ValueError as e:
        print(f"Classifier training failed: {e}", flush=True)
        return None
    return {'clf':clf, 'X':X, 'y':y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_models()
    return bool(model_data)


def predict_attendance(class_image_np):
    # Detect faces and extract their embeddings first.
    encodings = get_face_embeddings(class_image_np)
    num_faces = len(encodings)

    detected_student = {}

    # No face was detected by Dlib.
    if num_faces == 0:
        return {}, [], 0

    # Load the student recognition model.
    model_data = get_trained_models()

    # Faces exist even if no student model is available.
    if not isinstance(model_data, dict):
        return {}, [], num_faces

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = list(dict.fromkeys(y_train))

    if not X_train or not all_students:
        return {}, [], num_faces

    for encoding in encodings:
        # Find the closest stored embedding across all students.
        distances = [
            np.linalg.norm(stored_embedding - encoding)
            for stored_embedding in X_train
        ]

        best_index = int(np.argmin(distances))
        best_match_score = distances[best_index]
        closest_student_id = y_train[best_index]

        # Use the closest embedding as the match candidate.
        if best_match_score <= 0.6:
            if len(all_students) >= 2:
                predicted_id = clf.predict([encoding])[0]

                # Verify that the SVM prediction also has
                # a sufficiently close stored face embedding.
                predicted_indices = [
                    i for i, sid in enumerate(y_train)
                    if sid == predicted_id
                ]

                if predicted_indices:
                    predicted_distance = min(
                        np.linalg.norm(X_train[i] - encoding)
                        for i in predicted_indices
                    )

                    if predicted_distance <= 0.6:
                        detected_student[predicted_id] = True
            else:
                detected_student[closest_student_id] = True

    return detected_student, all_students, num_faces
