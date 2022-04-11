

from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from werkzeug.utils import secure_filename


# from django.core.files import default_storage
from . import Operations
import cv2
import json
# Create your views here.

#   Method to handle request for Retreiving the details of the scanned dendrite image. 
def post1(request):
    handler = Operations.Operations()
    print("Scan called")

    if request.method == 'POST':
        if request.FILES['file']:
            file = request.FILES['file']
        else:
            msg = "No file sent"
            return HttpResponse(json.dumps(msg))
        
        if file:
            
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            image = cv2.rotate(image,rotateCode=cv2.ROTATE_90_CLOCKWISE)
            resizeDIm = (int(image.shape[1]*20/100),int(image.shape[0]*20/100))
            image = cv2.resize(image,resizeDIm,interpolation=cv2.INTER_AREA)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            # cv2.imshow(" ",image)
            # cv2.waitKey(0)
            # file_name = default_storage.save(filename,file)
            
#       finding the image stored in database and retreiving the details of the image
        check = handler.image_Compare(image)
        if check != "No Match":
            data = handler.select_match(check[1])
            msg = {"Match":"1", 
                    "prodID": str(data[0]),
                    "brand":str(data[1]),
                    "disc":str(data[2]),
                    "cat":str(data[3]),
                    "mfg": str(data[4]),
                    "exp": str(data[5])
                    }
            return HttpResponse(json.dumps(msg))
        else:
            print("No match found")
            msg = {"Match":"-1"}
            return HttpResponse(json.dumps(msg))

# Method to handle request to register the captured dendrite image on database
def post2(request):
    print("Register called")
    handler = Operations.Operations()
    if request.method == 'POST':
        if request.FILES['file']:
            
            file = request.FILES['file']
        else:
            msg = "No file sent"
            
            return HttpResponse(json.dumps(msg))
        brand = request.POST.get("brnd")
        disc = request.POST.get("disc")
        cat = request.POST.get("cat")
        mfg = request.POST.get("mfgdate")
        exp = request.POST.get("expdate")
        
        if file:
            # flname = secure_filename(file.filename)
            
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            image = cv2.rotate(image,rotateCode=cv2.ROTATE_90_CLOCKWISE)
            resizeDIm = (int(image.shape[1]*20/100),int(image.shape[0]*20/100))
            image = cv2.resize(image,resizeDIm,interpolation=cv2.INTER_AREA)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            
            # file_name = default_storage.save(filename,file)

        hashofImg = handler.hash_function(image)
        img = handler.encode_img(image)
        task = (hashofImg,img,brand,disc,cat,mfg,exp)
#       checks if the captured image exists in database  
        check = handler.image_Compare(image)
        if (check == "No Match"):
            handler.insert_row(task)
            print("No Match found")
            msg = {"Match":"2"}
            return HttpResponse(json.dumps(msg))
        else:
            print("Match Found")
            msg = {"Match":"-1"}
            return HttpResponse(json.dumps(msg))

# method to handle the request to update the details of the stored dendrite 
def post3(request):
    print("Update Called")
    handler = Operations.Operations()
    if request.method == "POST":

        id = request.POST.get("id")
        brand = request.POST.get("brnd")
        disc = request.POST.get("disc")
        cat = request.POST.get("cat")
        mfg = request.POST.get("mfgdate")
        exp = request.POST.get("expdate")
        task=[id,brand,disc,cat,mfg,exp]
#       method to update record in database  
        handler.update_info(task)
        print("Record Updated")
#       method to retreive the updated record.
        data = handler.select_match(id)
        print(data[4]+" "+data[5])
        msg = {"Match":"3", 
                "prodID": str(data[0]),
                "brand":str(data[1]),
                "disc":str(data[2]),
                "cat":str(data[3]),
                "mfg": str(data[4]),
                "exp": str(data[5])
                }
        return HttpResponse(json.dumps(msg))

        
