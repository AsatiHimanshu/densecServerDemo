

from densecID.models import dendrites
import cv2
import numpy as np
from PIL import Image
import imagehash

# from django.core.files import default_storage

class Operations:

    def encode_img(self,image):
        # reduce size of image before storing
        image_str = cv2.imencode(".jpg",image)[1].tostring()
        return image_str

    def decode_img(self,image):
       
        image = np.frombuffer(image,np.uint8)
        image = cv2.imdecode(image,cv2.IMREAD_COLOR)
        return image
        
        # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)



    def hash_function(self,image):
        img_pil = Image.fromarray(image)
        im_hash = imagehash.whash(img_pil)
        return str(im_hash)

    def orb_Sim(self,imgA , imgB):
        orb = cv2.ORB_create()
        kpA, dsA = orb.detectAndCompute(imgA, None)
        kpB, dsB = orb.detectAndCompute(imgB, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(dsA,dsB)
        similar = [i for i in matches if i.distance<45]
        if len(matches) == 0:
            return 0
        return len(similar)/len(matches)*100

    def select_images(self,i):

        images = dendrites.objects.values_list("dendPic", flat=True)[i:i+20]
        hash = dendrites.objects.values_list("dendID",flat=True)[i:i+20]

        images = [self.decode_img(a) for a in images]
        return images,hash
        
    def image_Compare(self,image):
        scan = image
        den_images=[]
        den_sim=[]
        last = dendrites.objects.all().count()
        for i in range(0,last,20):
            images, hashes = self.select_images(i)
            # print(hashes)
            sim=[]
            
            if not images:
                # print("No match")
                return "No Match"
            
            else: 
                # print(len(images))
                # print("Something")
                
                for j in range(len(images)):
                    # print(j)
                    # cv2.imshow(" ",images[j])
                    # cv2.waitKey(0)
                    sim.append(self.orb_Sim(scan,images[j]))
                
                best_ind = sim.index(max(sim))
                den_images.append((images[best_ind],hashes[best_ind]))
                den_sim.append(sim[best_ind])
        if not den_sim:
            return "No Match"
        else:
            match = den_sim.index(max(den_sim))
            # print(den_sim)
            if (max(den_sim)<50):
                # print("similarity<50")
                return "No Match"
            else:
                # print("Hash",den_images[match][1])
                return den_images[match]

    # --------------------------------------------------------------------------------
        
    def insert_row(self,task):
        try:
            ins = dendrites(dendID = task[0], 
                            dendPic = task[1],                 
                            prod_name = task[2],
                            prod_disc = task[3],
                            prod_category = task[4],
                            mfg_date = task[5],
                            exp_date = task[6] )
            ins.save()
        except Exception as e:
            print("Error while inserting",e)
        

    

    def select_match(self,hash):
        try:
            match = dendrites.objects.filter(dendID = str(hash)).values()
            match = match[0]
            
            data=[match['dendID'],match['prod_name'],match['prod_disc'],match['prod_category'],match['mfg_date'],match['exp_date']]
            return data
        except Exception as e:
            print("Erreor in select match",e)

    def update_info(self,task):
        try:
            dendrites.objects.filter(dendID = str(task[0])).update(prod_name = str(task[1]),
                                                                prod_disc = str(task[2]),
                                                                prod_category = str(task[3]),
                                                                mfg_date = str(task[4]),
                                                                exp_date = str(task[5])) 
        except Exception as e:
            print("Error while updating database",e)