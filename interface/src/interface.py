# import the necessary packages
from cProfile import label
from curses import panel
from tkinter import *
from tkinter import ttk, font, filedialog, Entry
from tkinter.messagebox import askokcancel, showinfo, WARNING
import getpass
import base64

import tkinter.messagebox
from tkinter import messagebox

from turtle import clear
from urllib import request

import grpc
from PIL import Image
from PIL import ImageTk
import numpy as np

import backend_pb2
import backend_pb2_grpc

import inference_pb2
import inference_pb2_grpc

root = Tk()

panelA = None
srtPath = None

def run_model():
    global strPath, inference_client

    if len(strPath) > 0:

        path_msg = inference_pb2.img_path2(path=strPath)
        response2 = inference_pb2.predict(path_msg)

        v_percent = response2.percent
        v_result = response2.dataresult
        result_prediction = "El Resultado del Analisis de la imagen\n Presenta un tipo de neumonia {}, \n con una probabilidad de {:.2f}%".format(v_result, v_percent)

        messagebox.showinfo(title=None, message=result_prediction)

    else:

        messagebox.showerror('El path viene vacio')


    #text2.insert(END, v_result)
    #text3.insert(END, '{:2.f}'.format(v_percent) + '%')


def select_image():
    # grab a reference to the image panels
    global panelA, backend_client, strPath
    # open a file chooser dialog and allow the user to select an input
    # image
    #path = filedialog.askopenfilename()

    path = filedialog.askopenfilename(
            title="Select image",
            filetypes=(
                ("DICOM", "*.dcm"),
                ("JPEG", "*.jpeg"),
                ("jpg files", "*.jpg"),
                ("png files", "*.png"),
            )
    )

    # ensure a file path was selected
    if len(path) > 0:

        strPath = path
        path_message = backend_pb2.img_path(path=path)
        response = backend_client.load_image(path_message)

        img_content = response.img_content
        img_w = response.width
        img_h = response.height

        
        b64decoded = base64.b64decode(img_content)
        image = np.frombuffer(b64decoded, dtype=np.uint8).reshape(img_h, img_w, -1)
                
        # convert the images to PIL format...
        image = Image.fromarray(image)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)

        tamanio = (250, 250)

        image = image.resize(tamanio)

        image = ImageTk.PhotoImage(image)

        # if the panels are None, initialize them
        if panelA is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            #update button Predict
            button1['state'] = 'normal'

        else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image
        
        #button1['state'] = 'enable'

root.title("Detector Neumonia")
#root.geometry("490x560")
root.resizable(0, 0)

# fonti = font.Font(weight = 'bold')

# lab1 = ttk.Label(root, text = "Imagen readiologica", font=fonti)
# lab3 = ttk.Label(root, text = "Resultado", font=fonti)
# lab6 = ttk.Label(root, text = "Probabilidad", font=fonti)

# result = StringVar() 

# #Input boxes
# text2 = Text(root)
# text3 = Text(root)

# #buttons
# button1 = ttk.Button(root, text='Predecir', state='disable', command=run_model)
# button2 = ttk.Button(root, text='Cargar Imagen', command=select_image)

# #widget position
# lab1.place(x=110, y=65)
# lab3.place(x=80, y=370)
# lab6.place(x=80, y=415)
# button1.place(x=220, y=460)
# button2.place(x=70, y=460)
# text2.place(x=220, y=370, width=90, height=30)
# text3.place(x=220, y=415, width=90, height=30)

# initialize the window toolkit along with the two image panels
#root = Tk()
#panelA = None

# Backend client definition
maxMsgLength = 1024*1024*1024

# options = [('grpc.max_send_message_length', MAX_MESSAGE_LENGTH), 
# ('grpc.max_recive_message_length', MAX_MESSAGE_LENGTH)]
# channel = grpc.insecure_channel("backend:50051", options=options)
# backend_client = backend_pb2_grpc.BackendStub(channel=channel)

# #Inference definition
# channel2 = grpc.insecure_channel("backend:50052", options=options)
# inference_client = inference_pb2_grpc.InferenceStub(channel=channel2)

options = [('grpc.max_message_length', maxMsgLength), ('grpc.max_send_message_length', maxMsgLength), ('grpc.max_receive_message_length', maxMsgLength)]
channel = grpc.insecure_channel("backend:50051", options = options)
backend_client = backend_pb2_grpc.BackendStub(channel=channel)

#Inference definition
channel2 = grpc.insecure_channel("inference:50052")
inference_client = inference_pb2_grpc.InferenceStub(channel=channel2)


# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
button1 = Button(root, text="Predecir", state='disabled', command=run_model) 
button1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
#btn = Button(root, text="Select an image", command=select_image)
#btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()
