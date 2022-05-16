from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from .models import Result


from keras.models import load_model
from keras.preprocessing import image
import json 
import tensorflow as tf
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


img_height, img_width = 256, 256
with open('./models/labels.json', 'r') as f:
    labelInfo = f.read()

labelInfo = json.loads(labelInfo)
# print(labelInfo)

tf.compat.v1.disable_eager_execution()
model_graph = tf.Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()

    with tf_session.as_default():
        model=load_model('./models/model.h5')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def predictImage(request):
    # print(request)
    # print(request.POST.dict())

    try:

        fileObj = request.FILES['filePath']
        fs = FileSystemStorage()

        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.'+filePathName
        # print(testimage)
        # print(filePathName)

        # print(type(testimage))

        # if '%20' in testimage:
        #     testimage = fileObj.replace("%20", ' ')
        #     print(testimage)

        img = image.load_img(testimage, target_size=(img_height, img_width))
        test_image = image.img_to_array(img)
        test_image = np.expand_dims(test_image, axis = 0)

        confidence = 0
        with model_graph.as_default():
            with tf_session.as_default():
                pred = model.predict(test_image)
                # print(pred)
                confidence = round(np.max(pred) * 100, 2)

        predictedLabel = labelInfo[str(np.argmax(pred[0]))]
        print('Predicted label: ', predictedLabel)  
        print(f'Confidence : {confidence}%')    

        

        filename = filePathName.split('/')[-1]
        print(filePathName)

        new_item = Result(imagepath = filePathName, image = filename, predicted = predictedLabel, confidence = confidence)
        new_item.save()

        context = {'filePathName':filePathName, 'predictedLabel': predictedLabel, 'confidence': confidence, 'filename': filename}
        return render(request, 'index.html', context)

    except:
        return render(request, 'index.html')


def viewDataBase(request):
    all_results = Result.objects.all()

    # listOfImages = os.listdir('./media/')
    # listOfImagesPath = ['./media/' + i for i in listOfImages]
    context = { 'all_results':all_results}  #  'listOfImagesPath': listOfImagesPath,
    return render(request, 'viewDB.html', context)