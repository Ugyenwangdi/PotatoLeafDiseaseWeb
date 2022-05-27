from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


from django.core.files.storage import FileSystemStorage
from .models import Result, APIResult
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LeafDiseaseSerializer, APILeafDiseaseSerializer

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




# def register(request):

#     if request.method == 'POST':
        
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if username and email and password1 and password2:
#             if password1 == password2:
#                 if User.objects.filter(username=username).exists():
#                     messages.info(request, 'Username taken...')
#                     return render(request, 'register.html')

#                 elif User.objects.filter(email=email).exists():
#                     messages.info(request, 'Email taken...')
#                     return render(request, 'register.html')

#                 else:
#                     user = User.objects.create_user(username=username, password=password1, email=email)
#                     user.save()
#                     messages.info(request, 'User created')
#                     return render(request, 'index.html')
#             else:
#                 messages.info(request, 'Password did not match..')
#             return render(request, 'register.html')

#         else:
#             messages.info(request, 'Fill all the fields')
#             return render(request, 'register.html')
#     else:
#         return render(request, 'register.html')



# def loginUser(request):
    
#     if request.user.is_authenticated:
#         return redirect('classifierApp:homepage')

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('classifierApp:homepage')
#         else:
#             return render(request, 'login.html', {'error': 'It seems you entered wrong details.'})

#     return render(request, 'login.html')

# def changePW(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
        
#         try:
#             user = User.objects.get(username=username)
            
#             if username and password1 and password2:
#                 if password1 == password2:
#                     user.set_password(password1)
#                     user.save()
#                     return redirect('classifierApp:homepage')
#                 return render(request, 'change_password.html', {'error': 'Passwords did not match'})
#         except:
#             return render(request, 'change_password.html', {'error': 'could not find the details'})
#     return render(request, 'change_password.html')

# def logoutUser(request):
#     logout(request)
#     return redirect('classifierApp:homepage')


# Create your views here.
def home(request):
    return render(request, 'index.html')

def indexm(request):
    return render(request, 'indexm.html')

def history(request):
    # if not request.user.is_authenticated:
    #     return redirect('classifierApp:login')


    all_results = Result.objects.all()

    image = ''
    predicted = ''
    imagelink = ''
    confidence = ''
    saved = ''
    src = ''
    earlyblight = False
    lateblight = False 
    healthy = False
    unknown = False

    for i in all_results:
        image = i.image
        predicted = i.predicted
        imagelink = i.imagelink
        confidence = i.confidence
        saved = i.saved
        src = i.imagepath 

        if predicted == "Early Blight":
            earlyblight = True
        
        elif predicted == "Late Blight":
            lateblight = True 

        elif predicted == "Healthy":
            healthy = True 

        else:
            unknown = True

    # for i in all_results:
    #     print(i.imagepath)
    #     break

    # listOfImages = os.listdir('./media/')
    # listOfImagesPath = ['./media/' + i for i in listOfImages]
    context = { 
        "image" : image,
        "predicted" : predicted,
        "imagelink" : imagelink,
        "confidence" : confidence,
        "saved" : saved,
        "src" : src, 
        "earlyblight": earlyblight,
        "lateblight" : lateblight,
        "healthy" : healthy,
        "unknown": unknown


        
    }  #  'listOfImagesPath': listOfImagesPath,
    return render(request, 'history.html', context)

def predictImage(request):
    # print(request)
    # print(request.POST.dict())

    all_results = Result.objects.all()

    all_results.delete()

    earlyblight = False
    lateblight = False 
    healthy = False
    unknown = False


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

        if predictedLabel == "Early Blight":
            earlyblight = True
        
        elif predictedLabel == "Late Blight":
            lateblight = True 

        elif predictedLabel == "Healthy":
            healthy = True 

        else:
            unknown = True

        

        filename = filePathName.split('/')[-1]
        print(filename)

        new_item = Result(imagepath = filePathName , imagelink = 'https://potatoleafdisease.herokuapp.com'+filePathName, image = filename, predicted = predictedLabel, confidence = confidence)
        new_item.save()

        context = {'filePathName':filePathName, 'predictedLabel': predictedLabel, 'confidence': confidence, 'filename': filename, 'earlyblight' : earlyblight, 'lateblight' : lateblight, 'healthy' : healthy, 'unknown' : unknown}
        return render(request, 'index.html', context)

    except:
        return render(request, 'index.html')


def viewDataBase(request):

    # if not request.user.is_authenticated:
    #     return redirect('classifierApp:login')


    all_results = Result.objects.all()
    # for i in all_results:
    #     print(i.image.url)
    #     break

    # for i in all_results:
    #     print(i.imagepath)
    #     break

    # listOfImages = os.listdir('./media/')
    # listOfImagesPath = ['./media/' + i for i in listOfImages]
    context = { 'all_results':all_results}  #  'listOfImagesPath': listOfImagesPath,
    return render(request, 'viewDB.html', context)




########## API ############

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/routes',
            'method': 'Get',
            'description': 'Return all the api routes'
        },
        {
            'Endpoint': '/api/results/all',
            'method': 'Get',
            'description': 'Returns all the predicted results stored in database'
        },
        {
            'Endpoint': '/api/predict',
            'method': 'Post',
            'description': 'Use this endpoint to predict the new class of an image'
        }
    ]

    return Response(routes)


# API endpoints
class PotatoAPIView(APIView):

    # get results from the database of website
    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('classifierApp:login')

        saved_results = APIResult.objects.all()


        serializer = LeafDiseaseSerializer(saved_results, many=True)
        # print(serializer.data)

        return Response({"results": serializer.data})

    # post image and predict the class of an image
    def post(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('classifierApp:login')
        
        # empty the database before prediction on new image
        records = APIResult.objects.all()
        records.delete()
        
        imagename = request.data.get('imagename')

        fileObj = request.FILES['image']
        fs = FileSystemStorage()

        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.'+filePathName

        # print(testimage)

        img = image.load_img(testimage, target_size=(img_height, img_width))
        test_image = image.img_to_array(img)
        test_image = np.expand_dims(test_image, axis = 0)
        
        confidence = 0
        with model_graph.as_default():
            with tf_session.as_default():
                cnn_pred = model.predict(test_image)

                # print(pred)
                confidence = round(np.max(cnn_pred) * 100, 2)

        predictedLabel = labelInfo[str(np.argmax(cnn_pred[0]))]
        print('Predicted label: ', predictedLabel)  
        print(f'Confidence : {confidence}%')    
    

        filename = filePathName.split('/')[-1]
        print(filename)

        new_item = APIResult(imagename = imagename, imagelink = 'https://potatoleafdisease.herokuapp.com'+filePathName, image = filename, predicted = predictedLabel, confidence = confidence)
        new_item.save()


        api_results = APIResult.objects.all()

        

        serializer = APILeafDiseaseSerializer(api_results, many=True)

        return Response({"results": serializer.data})
