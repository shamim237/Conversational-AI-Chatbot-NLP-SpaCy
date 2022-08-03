import requests


def picture_url(file_name, type, pharmacyId, token):
    headers = { "Authorization": "Bearer " + str(token)}
    multipart_form_data = {'file': (file_name, open(file_name, 'rb')),'type': type}
    res = requests.post(url='https://jarvin-dev.azurewebsites.net/api/Media/Upload/{}'.format(pharmacyId), headers=headers, files=multipart_form_data)

    dictFromServer = res.json()
    url = dictFromServer['response']['pictureUrl']
    id = dictFromServer['response']['pictureId']
    return url, id