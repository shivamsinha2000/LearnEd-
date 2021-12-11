from google.cloud import firestore
import os
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import EntitiesOptions,KeywordsOptions,Features, CategoriesOptions

from google_images_download import google_images_download
from imagesoup import ImageSoup
###########################NLP_API_KEY######################################
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='Enter Your API Key here',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)
###############################FIRESTORE_API_KEY############################
path=r"C:\Users\Harsha Chowdary\Downloads\codeSpace.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =path

db = firestore.Client()
doc_ref_s1 = db.collection(u'NLP').document(u'KeyWOrds')
doc_ref_s2 = db.collection(u'NLP').document(u'Sentence')
doc_ref_s3 = db.collection(u'NLP').document(u'Image_URL')
doc_image=db.collection(u'database').document(u'book2').collection(u'nlp').document(u'image')
doc_keywords=db.collection(u'database').document(u'book2').collection(u'nlp').document(u'keywords')
doc_sentence=db.collection(u'database').document(u'book2').collection(u'nlp').document(u'sentence')
doc_no_of_sentence=db.collection(u'database').document(u'book2')
t1="The nurse checking your vitals has plans. You’ve been in the hospital long enough to know the shift is almost over.Soon another person in a lime uniform will come into your room, erase this nurse’s name from the tiny whiteboard and write in their own.You hope it’s Sam, who’s quick with the dirty jokes and quicker still with the dilaudid, the good stuff."
str_=""
li=[]
for i in t1:
  if(i!='.' and i!='?' and i!='!'):
    str_+=i
  else:
    li.append(str_)
    str_=""
l=len(li)
print(li)
print(l)
########################iniatialize IMageSOUP###########################
imgsrch = ImageSoup()

for i in range(0,l):
  print(li[i])
  
  response = natural_language_understanding.analyze(
      text=li[i],
      features=Features(keywords=KeywordsOptions())).get_result()
  data = response
  #print(response)
  doc_sentence.update({str(i+1):li[i]})   
  
  #absolute_image_paths = response_1.download(arguments)
  for p in data['keywords']:
    print('TEXT: ' + p['text'])
    doc_keywords.update({str(i+1): p['text']})
    images = imgsrch.search(p['text'], n_images=1)
    url=images[0].URL    
    doc_image.update({str(i+1):url})  




