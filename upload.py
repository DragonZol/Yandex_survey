import json
import requests

def upload_json_to_yandex_disk(state):
    json_data = {'results': state}
    file_name = 'data.json'
    yandex_disk_token = 'y0_AgAAAABNWZOrAAtrUQAAAAD9wo8DAACEP7UX46JHGKIS8dDwccA7sDbE7A'
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Authorization': f'OAuth {yandex_disk_token}'}
    params = {'path': file_name, 'overwrite': 'true'}
    files = {'file': json.dumps(json_data, ensure_ascii=False)}

    response = requests.get(upload_url, headers=headers, params=params)
    upload_data = response.json()  # Получаем данные для загрузки файла
    upload_url = upload_data['href']  # Получаем URL для загрузки файла

    response = requests.put(upload_url, files=files)
    if response.status_code == 201:
        print("JSON успешно загружен на Яндекс Диск.")
    else:
        print("Ошибка при загрузке JSON на Яндекс Диск:", response.text)


def upload_post(state):
    url = 'https://functions.yandexcloud.net/d4ei2d94t39iaompfhs8'
    headers = {'Content-Type': 'application/json'}

    try:
        data_json = json.dumps(state, ensure_ascii=False).encode('utf-8')
        print("Отправляемые данные:", data_json)

        response = requests.post(url, data=data_json, headers=headers)
        response.raise_for_status()  # Проверяем, был ли успешным запрос

        print("Ответ сервера:", response.text)

        return {
            "statusCode": response.status_code,
            "body": response.text
        }
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке POST запроса:", str(e))
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }