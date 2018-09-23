from src.helpers.auth import auth
import requests
import io
import zipfile
import tempfile
import re
import sys

api = auth()

test = api.mentions_timeline()
status = test[0]

if 'media' in status.extended_entities:
    screen_name = status.user.screen_name

    media = status.extended_entities['media'][0]

    if media['type'] == 'photo':
        m = re.search('^(@.+?)\s+?(.*)\s+?(http.+?)$', status.text)

        try:
            name = m.group(2)
        except:
            name = 'Cat'

        response = requests.get(media['media_url'])
        if response.status_code == 200:
            cattac_response = requests.post(
                'http://localhost:8080/cattac',
                files={
                    'image': io.BytesIO(response.content).getvalue()
                },
                data={
                    'name': name
                }
            )

            text = status.text

            media_ids = []
            tweet = '.@'+screen_name+' ✨'

            with zipfile.ZipFile(io.BytesIO(cattac_response.content), 'r') as f:
                for name in f.namelist():
                    m = re.search('^.*_(.*)\.jpg$', name)
                    cat_name = m.group(1)

                    tweet += "\n"+'- '+cat_name

                    file = tempfile.NamedTemporaryFile(suffix='.jpeg')
                    file.write(f.read(name))
                    res = api.media_upload(file.name)
                    media_ids.append(res.media_id)

            api.update_status(status=tweet, media_ids=media_ids)
