import json
from nltk.tokenize import word_tokenize
import string
from nltk import FreqDist
from nltk.corpus import stopwords
import boto3
import json
from nltk.tokenize import word_tokenize


client = boto3.client('s3')
BUCKET_NAME = "optimizewords3"
# The object key or key name uniquely identifies the object in an AWS S3 bucket
BUCKET_OBJECT_KEY_NAME = "File_WordClouds.json"
# for specifying the file path
LOCAL_FILE_PATH = r'C:\Users\Entropik\serverless_framework\wordcloud\WordCloud1.json'


def nltk_word_cloud(payload):
    # Word tokenization is the process of splitting a large sample of text into words.
    # This is a requirement in natural language processing tasks where each word needs to be captured
    stop_words = set(stopwords.words('english'))
    text = word_tokenize(payload)
    print(text)
    ListOfWords = []
    ListOfWords = [token for token in word_tokenize(payload) if token.lower() not in stop_words]
    print(ListOfWords)
    # new_string = text.translate(str.maketrans('', '', string.punctuation))
    # stop_list = set(stopwords.words('english') + list(new_string))
    #
    # tokens = [token for token in word_tokenize(new_string) if token.lower() not in stop_list]
    # word_data = FreqDist(tokens).most_common(25)
    nltk_load = s3_get_payload()
    # If a word already exists in file then the new counts needs to be added to the existing word count.
    # If the new word not already exists in file, then this new word needs to be added to the S3 file.
    for word in ListOfWords:
        if word in nltk_load:
            nltk_load[word] = nltk_load.get(word) + 1
        elif word not in nltk_load:
            nltk_load[word] = 1
    sorted_dict = dict(sorted(nltk_load.items(), key=lambda item: item[1], reverse=True))
    # Writing File
    imple_file = open(LOCAL_FILE_PATH, 'w')
    # It is used to write a Python object into a file as a JSON formatted data.
    json.dump(sorted_dict, imple_file, indent=3)
    # File close
    imple_file.close()
    # function call for uploading file to s3
    word_cloud_upload()
    # return top 25 words from this file as response
    output = {k: sorted_dict[k] for k in list(sorted_dict)[:25]}
    return {"statusCode": 200, "body": json.dumps(output)}


def s3_get_payload():
    try:
        s3bucket_object = client.get_object(Bucket=BUCKET_NAME, Key=BUCKET_OBJECT_KEY_NAME)
    except Exception as e:
        print("S3 File not found"+str(e))
        return {}
    File = s3bucket_object['Body'].read()
    # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary
    nltk_load = json.loads(File)
    return nltk_load


def word_cloud_upload():
    client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, BUCKET_OBJECT_KEY_NAME)
