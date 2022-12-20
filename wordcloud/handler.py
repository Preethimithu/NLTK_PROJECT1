from nltkfile import nltk_word_cloud
import json


def optimise_word_handler(request, context):
    print(context)
    payload = json.loads(request.get('body'))
    payload = payload.get('text')
    print("Running.....")
    return nltk_word_cloud(payload)
