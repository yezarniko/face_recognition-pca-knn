from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import numpy as np
from data import LoadData
import pickle as pk
from face_detect import getDataFromCamera
import cv2


def knn(neighbor, traindata, trainlabel, testdata):
    neigh = KNeighborsClassifier(n_neighbors=neighbor)
    neigh.fit(traindata, trainlabel)
    return neigh.predict(testdata)


IMAGE_SIZE = 224
color = (0, 255, 0)

users = [
    "",
    "ye zar ni ko",
    "thet nyein chan lwin",
    "aung htet oo"
]


Data, Label = LoadData()
Data = np.asarray(Data)
Label = np.asarray(Label)

with open("pca.pkl", "rb") as pca_file:
    pca = pk.load(pca_file)

with open("trainDataS.pkl", "rb") as trainDataS_file:
    trainDataS = pk.load(trainDataS_file)


def test(img_test, frame, faceRect):
    img_test = np.reshape(img_test, (1, IMAGE_SIZE * IMAGE_SIZE))
    testDataS = pca.transform(img_test)

    #****** KNN *******
    result = knn(5, trainDataS, np.asarray(Label), testDataS)
    #****** KNN *******

    faceID = result[0]
    print(users[faceID])


    x, y, w, h = faceRect

    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)

    cv2.putText(frame, users[faceID],
                (x + 30, y + 30),                      
                cv2.FONT_HERSHEY_SIMPLEX,              
                1,                                     
                (255,0,255),                           
                2)                                     


    cv2.imshow("find me", frame)
getDataFromCamera(test)