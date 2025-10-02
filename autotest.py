FOLDER = 'data' # директория, в которую нужно положить ZIP-архивы
LOGIN = 'admin'
PASSWORD = "ваш пароль" # введите пароль, который используется для доступа к сайту
HOST = "mediside.ru"
COLLECTION_ID_FILE = 'collection_id.txt' # файл нужен, чтобы не создавать каждый раз новую коллекцию, а работать с существующей
# в случае возникновения ошибок попробуйте его удалить

import os
import http.client
import mimetypes
import base64
import uuid
import json

def create_multipart_form_data(field_name, filename, file_content):
    boundary = uuid.uuid4().hex
    content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    data = []
    data.append(f'--{boundary}')
    data.append(f'Content-Disposition: form-data; name="{field_name}"; filename="{os.path.basename(filename)}"')
    data.append(f'Content-Type: {content_type}')
    data.append('')
    data.append(file_content)
    data.append(f'--{boundary}--')
    data.append('')

    body = b'\r\n'.join(item if isinstance(item, bytes) else item.encode() for item in data)
    content_type_header = f'multipart/form-data; boundary={boundary}'
    return content_type_header, body

def upload_file(file_path, collection_id):
    with open(file_path, 'rb') as f:
        file_content = f.read()

    content_type, body = create_multipart_form_data('files', file_path, file_content)

    auth = f"{LOGIN}:{PASSWORD}"
    auth_encoded = base64.b64encode(auth.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": content_type,
        "Content-Length": str(len(body))
    }

    conn = http.client.HTTPSConnection(HOST)
    conn.request("POST", '/api/v1/researches/upload?collection_id='+collection_id, body=body, headers=headers)
    response = conn.getresponse()
    print(f"Upload {os.path.basename(file_path)}: {response.status} {response.reason}")
    conn.close()

def create_collection() -> str:
  auth = f"{LOGIN}:{PASSWORD}"
  auth_encoded = base64.b64encode(auth.encode()).decode()
  headers = { "Authorization": f"Basic {auth_encoded}" }

  conn = http.client.HTTPSConnection(HOST)
  conn.request("POST", "/api/v1/collections/new", headers=headers)
  response = conn.getresponse()
  collection_data = response.read().decode()
  print(f"create collection result: {response.status} {response.reason} {collection_data}")
  conn.close()
  return json.loads(collection_data)['id']

try:
  with open(COLLECTION_ID_FILE, "r", encoding="utf-8") as f:
      collection_id = f.read()
      print(f'collection id found in {COLLECTION_ID_FILE} file')
except FileNotFoundError as e:
    print(f'{COLLECTION_ID_FILE} not found, try create collection')
    collection_id = create_collection()
    with open(COLLECTION_ID_FILE, "x", encoding="utf-8") as f:
        f.write(collection_id)

print('collection id:', collection_id)
print('You can open this collection in browser:', f'http://{HOST}/collections/{collection_id}')

print('Start upload files, please, wait...')
for filename in os.listdir(FOLDER):
    file_path = os.path.join(FOLDER, filename)
    if os.path.isfile(file_path):
        upload_file(file_path, collection_id)
