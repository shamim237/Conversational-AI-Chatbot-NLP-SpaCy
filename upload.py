import requests


def picture_url(file_name, type, pharmacyId, token):
    headers = { "Authorization": "Bearer " + str(token)}
    multipart_form_data = {'file': (file_name, open(file_name, 'rb')),'type': type}
    res = requests.post(url='https://jarvin-dev.azurewebsites.net/api/Media/Upload/{}'.format(pharmacyId), headers=headers, files=multipart_form_data)

    dictFromServer = res.json()
    url = dictFromServer['response']['pictureUrl']
    id = dictFromServer['response']['pictureId']
    return url, id

# def picture_id(file_name, type):
#     multipart_form_data = {'file': (file_name, open(file_name, 'rb')),'type': type}
#     res = requests.post(url='https://jarviscare.azurewebsites.net/api/Media/Upload/1',
#                         files = multipart_form_data,
#                         headers=headers)
#     dictFromServer = res.json()
#     print(dictFromServer)
#     response = dictFromServer['response']['pictureId']
#     return response

# ss = picture_url('Picture2.jpg', 'image/jpg')
# print(ss)