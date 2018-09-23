from src.helpers.auth import auth
import requests
import io
import zipfile
import tempfile

api = auth()

test = api.mentions_timeline()
status = test[0]

if 'media' in status.extended_entities:
    screen_name = status.user.screen_name

    media = status.extended_entities['media'][0]

    if media['type'] == 'photo':
        response = requests.get(media['media_url'])
        if response.status_code == 200:
            cattac_response = requests.post(
                'http://localhost:8080/cattac',
                files={
                    'image': io.BytesIO(response.content).getvalue()
                },
                data={
                    'name': 'testtest'
                }
            )

            media_ids = []
            with zipfile.ZipFile(io.BytesIO(cattac_response.content), 'r') as f:
                for name in f.namelist():
                    print(name)
                    file = tempfile.NamedTemporaryFile(suffix='.jpeg')
                    file.write(f.read(name))
                    res = api.media_upload(file.name)
                    media_ids.append(res.media_id)

            api.update_status(status='.@'+screen_name+' ✨', media_ids=media_ids)




