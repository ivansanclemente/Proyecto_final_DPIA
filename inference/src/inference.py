import csv
import numpy as np
import cv2

import grpc

import tensorflow as tf
from tensorflow.keras import models
from concurrent import futures

import inference_pb2
import inference_pb2_grpc



class InferenceService(inference_pb2_grpc.InferenceServicer):
    def _read_img(self, path):
        img = cv2.imread(path)
        img_array = np.asarray(img)
        img2 = img.array.astype(float)
        img2 = (np.maximum(img2,0) / img2.max()) * 255.0
        img2 = np.unit8(img2)

        return img2

    def predict (self, request, context):
        #load image
        path = request.path
        array = self._read_img(path=path)

        patch_array_img = self.preprocess(array)

        #Up model
        modelo = self.modelo()

        prediction = np.argmax(modelo.predict(patch_array_img))

        fit_percent = np.max(modelo.predict(patch_array_img))* 100
        str_dataresult = ''
        if prediction == 0:
            str_dataresult = "bacteriana"
        if prediction == 1:
            str_dataresult = "normal"
        if prediction == 2:
            str_dataresult = "viral"

        reponse_message = inference_pb2.datapred(percent = fit_percent, dataresult = str_dataresult)
        return reponse_message

    def preprocess(array):
        array = cv2.resize(array, (512, 512))
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        array = clahe.apply(array)
        array = array / 255
        array = np.expand_dims(array, axis=-1)
        array = np.expand_dims(array, axis=0)
        return array

    def model(self):
        model_cnn = tf.keras.models.load_model('WilhemNet_86.h5')
        return model_cnn

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InferenceServicer_to_server(InferenceService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

