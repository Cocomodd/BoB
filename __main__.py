from src.helpers.auth import auth
import requests
import io
import zipfile
import tempfile
import re
import sqlite3
from src.classes.models.tweet import Tweet

api = auth()

tweets = api.favorites()

conn = sqlite3.connect('kitty.db')
c = conn.cursor()

for status in tweets:
    if hasattr(status, 'extended_entities') \
            and 'media' in status.extended_entities \
            and status.extended_entities['media'][0]['type'] == 'photo':

        api.destroy_favorite(status.id)

        tweet = Tweet(status.id)

        if not tweet.exists():
            tweet.create()
        else:
            continue

        screen_name = status.user.screen_name
        media = status.extended_entities['media'][0]

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
