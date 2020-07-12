# EmotionDetection
This is final project for graduate, and it's only half part of whole completed project

## Description
This project can detect video or stream, there are up to 7 emotion can be classfied

### Steps
1. First step is trying to get as many image data as we can
2. Normalize all the image data to the same size and grayscale
3. Training the model based on preprocessed image data
4. Predict outcome on video or stream

## Function

### Image crawl
1. Execute `imageScraper.py` and you can type in query string to search on google chrome, multiple query string is seperated by space
2. Execute `getUrls.js` to scanf through the google image page and get all of **ORIGINAL** (not compressed) image urls, and then links will be saved as txt
3. Execute `imageDownloader.py` to download parallelly all image based on the previous txt file, the output will store in a dir


###  Image Preprocess
1. Execute `faceCutter.py` for cut out the face part parallelly, and it will save as a grayscale image
2. Execute `manualClassifier.py` to select a dir to classify images into 7 different categories
3. Execute `dataAugmentation.py` to rotate, flip, shear to increment our image dataset

### Training

1. Execute `emotionTrain.py` to set up a model and train, the model's struture is in `emotionNetwork.py`

### Dectection

1. Execute `realTimeEmotionDetection.py` for stream like web cam or other, this program will skip some frame to increase performance
2. Execute `videoEmotionDetection.py` for video, this program is parallel and slightly complicated structure that use semaphor, thread and lock
3. Execute `estimate.py` to see the overall accuracy of the result

## Demo
### Raw image
![raw image](https://i.imgur.com/rgyjWJh.png)

### Processed image
![processed image](https://i.imgur.com/7LQVlXe.png)

### Result image
![result image](https://i.imgur.com/hJh0spO.jpg)

