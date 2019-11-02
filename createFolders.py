import os
import shutil
import random
import glob
import numpy as np
import keras
from keras import backend as k
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense,Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
#%matplotlib inline



def createFolder():
    
    path_tarin="/home/orr/GuyCNN/Train"
    path_valid="/home/orr/GuyCNN/Valid"
    path_folder="/home/orr/GuyCNN/Dekel"
    #get all the names in the folder
    name=[]
    name=[x[0] for x in os.walk(path_folder)]
    correct_name=[]
    for i in range (1,len(name)):
        allMustName=name[i].split('/')[5]
        correct_name.append(allMustName)
    # print(allMustName)
    #os.mkdir(path_tarin)
    #os.mkdir(path_test)
    #print(correct_name)
    for my_name in correct_name:
        try:
            os.mkdir(path_tarin+'/'+str(my_name))
            os.mkdir(path_valid+'/'+str(my_name))
        except OSError:
           print("failure")
        else:
           print("succ")    
    return correct_name


def sectionImg(imgfile,trainLocation,testLocation):
    print(imgfile)
    mylist=[f for f in glob.glob(str(imgfile)+"**/*.jpg")]
    sizeToTest=len(mylist)//3
    print(sizeToTest)
    for i in range(1,sizeToTest):
        my_random_img=random.choice(mylist)
        print(my_random_img)
        try:
            shutil.move(my_random_img,testLocation)
        except:
            print('Dont cut')    
        mylist.remove(my_random_img)
    for i in range(0,len(mylist)):
        my_random_img=random.choice(mylist)
     #   print(my_random_img)
        try:
            shutil.move(my_random_img,trainLocation)
        except:
            print('Dont cut')     
            mylist.remove(my_random_img)


def MyCNN(myNames):
    valid_folder="/home/orr/FamilyCNN/Valid"
    test_folder="/home/orr/FamilyCNN/Test"
    train_folder="/home/orr/FamilyCNN/Train"
    train_batches=ImageDataGenerator().flow_from_directory(train_folder,target_size=(224,224),classes=myNames,batch_size=10)
    valid_batches=ImageDataGenerator().flow_from_directory(valid_folder,target_size=(224,224),classes=myNames,batch_size=10)
    test_batches=ImageDataGenerator().flow_from_directory(test_folder,target_size=(224,224),classes=myNames,batch_size=10)
    
    model=Sequential([
        Conv2D(32,(3,3),activation='relu',input_shape=(224,224,3)),Flatten(),
        Dense(8,activation='softmax'),
        ])
    model.compile(Adam(lr=.0001),loss='categorical_crossentropy',metrics=['accuracy'])
    model.fit_generator(train_batches,steps_per_epoch=200,validation_data=valid_batches,validation_steps=4, epochs=4,verbose=2)
    model.save('Laniado.h5')
    

    
def TestMyModel(myNames):
    new_model=load_model('/home/orr/hello/Dekel.h5')
    alon_file='/home/orr/GuyCNN/Test/y.jpg'
    alon_img=image.load_img(alon_file,target_size=(224,224))
    alon_img=image.img_to_array(alon_img)
    alon_img=np.expand_dims(alon_img,axis=0)
    alon_img/=224
    x_class=new_model.predict_classes(alon_img)
    print(new_model.predict(alon_img))
    print(x_class)
    index_1=(str(x_class)).split('[')[1]
    index=(str(index_1)).split(']')[0]
    print(int(index))
    print(myNames)
    print(myNames[int(index)])



def strat():
    myNames=[]
    #create Folder
    myNames=createFolder()
    print(myNames)
   # path_folder="/home/orr/FamilyCNN/Laniado"
   # test_folder="/home/orr/FamilyCNN/Valid"
   # train_folder="/home/orr/FamilyCNN/Train"
    #create Image
   # for name in myNames:
   #     sectionImg(path_folder+'/'+str(name),train_folder+'/'+str(name),test_folder+'/'+str(name))
   # MyCNN(myNames)
    TestMyModel(myNames)

    #
   # for name in myNames:
   #     sectionImg(path_folder+'/'+str(name),train_folder+'/'+str(name),test_folder+'/'+str(name))
if __name__ == "__main__":
    strat()


 
    

    

