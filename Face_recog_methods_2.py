#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import face_recognition as fr
import cv2
import os
import pickle
import numpy as np

class FaceRecognition:
    def __init__(self, frames_dir, known_face_encodings, student_dic):
        self.frames_dir = frames_dir
        self.known_face_encodings = known_face_encodings
        self.students = student_dic

        csm_students = list(self.students.keys())

    def load_image_paths(self):
        image_paths = [os.path.join(self.frames_dir, filename) for filename in os.listdir(self.frames_dir) if filename.lower().endswith('.jpg')]
        return image_paths
    
    def load_new_student(path):
        x_image = fr.load_image_file(path)
        x_face_encoding = fr.face_encodings(x_image)[0]
        return x_face_encoding

    def find_faces(self, image_paths):
        face_locations = []
        face_encodings = []

        for path in image_paths:
            frame = fr.load_image_file(path)
            rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

            face_locations = fr.face_locations(rgb_frame, number_of_times_to_upsample=1, model='hog')
            face_encodings_for_frame = fr.face_encodings(frame, face_locations)

            face_encodings.extend(face_encodings_for_frame)

        return face_encodings



    def cosine_similarity(self, vector_a, vector_b):
        vector_a = np.array(vector_a, dtype=float)
        vector_b = np.array(vector_b, dtype=float)
        dot_product = np.dot(vector_a, vector_b)
        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        cosine_similarity_value = dot_product / (magnitude_a * magnitude_b)
        return cosine_similarity_value

    def compare_faces(self, video_face_encodings):
        similarities = []
        student_names = []
        csm_students = list(self.students.keys())

        for y in video_face_encodings:
            nec = [self.cosine_similarity(y, x) for x in self.known_face_encodings]
            similarities.append(nec)

        for x in similarities:
            student_names.append(csm_students[np.argmax(x)])

        return list(set(student_names))

