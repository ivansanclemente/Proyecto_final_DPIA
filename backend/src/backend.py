from concurrent import futures
import base64
from turtle import width
from PIL import ImageTk, Image

import grpc
import cv2
#import numpy as np

#import tensorflow as tf

import backend_pb2
import backend_pb2_grpc

#import inference_pb2
#import inference_pb2_grpc

class BackendService(backend_pb2_grpc.BackendServicer):
    def _test_func(self, path):
        image = cv2.imread(path)
        h, w, _ = image.shape
        print(f"image shape: w-{w} h-{h}")

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (250, 250), interpolation = cv2.INTER_AREA)
        #image = cv2.resize(image,250, 250, interpolation = cv2.INTER_AREA)
        image_str = base64.b64encode(image)
        return image_str, w, h

    def load_image(self, request, context):
        # load the image from disk
        path = request.path
        print(path)

        image_str, w, h = self._test_func(path=path)

        response_message = backend_pb2.image(img_content=image_str, width=w, height=h)
        return response_message

       

def serve():
    maxMsgLength = 1024 * 1024 * 1024
    options = [('grpc.max_message_length', maxMsgLength),('grpc.max_send_message_length', maxMsgLength),('grpc.max_receive_message_length', maxMsgLength)]


    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_BackendServicer_to_server(BackendService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
