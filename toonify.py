#librerias necesarias (
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import cv2 
import requests
import urllib.request
from urllib.request import urlopen
import numpy as np
import time
import io
# )

width=600
height=600
dim=(width, height)
api_key= "7666239e-5d9d-4aef-a8a6-36bcefea19e6"
api_url = "https://api.deepai.org/api/toonify"
def select_image(): 
    global panelA, panelB
    path = tkFileDialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        image=cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        loading= Label(root,text='cargando', foreground='yellow', background='white')
        loading.pack(side="top", padx=10, pady=10)
        loading.update_idletasks()
        #hacemos la consulta a la api
        r = requests.post(api_url,
files={'image': open(path, 'rb'),},headers={'api-key': api_key})
        out = r.json()
        out_img= out['output_url']
        img =Image.open(urlopen(out_img))
        new_img =img.resize((width,width),Image.ANTIALIAS)
        filename = os.path.basename(path)
        print(filename)
        new_img.save('out_'+filename,'jpeg')
        new_img.save('out_image.jpg','jpeg')
        imageB = cv2.imread('out_image.jpg')
        imageB=cv2.resize(imageB, dim, interpolation = cv2.INTER_AREA)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2RGB)
        imageB = Image.fromarray(imageB)
        imageB = ImageTk.PhotoImage(imageB)
        if panelA is None or panelB is None:
            panelA = Label(image=image) 
            panelA.image = image 
            panelA.pack(side="top", padx=10, pady=10)
            panelB = Label(image=imageB) 
            panelB.image = imageB
            panelB.pack(side="bottom", padx=10, pady=10)
            loading.config(text = "Hecho", foreground='green', background='white')
            loading.update_idletasks()
        else:
            panelA.configure(image=image) 
            panelB.configure(image=imageB) 
            panelA.image = image 
            panelB.image = imageB
            loading.config(text = "No funcionó", foreground='red', background='white')
            loading.update_idletasks()
            
root = Tk()
root.configure(background='white')
panelA = None
panelB = None
title= Label(root, text="Toonify by DeepAi", foreground='blue',background='white')
title.pack(side="top", expand="no", pady="10")
btn = Button(root, text="Elegir imagen", command=select_image)
btn.pack(side="bottom", fill="both", expand="no", padx="10", pady="10") 

root.mainloop()