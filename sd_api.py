import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin


def stable_diffusion(prompt, filename):
    url = "http://localhost:7861"

    payload = {
        "prompt": prompt,
        "steps": 20,
        "batch_size": 4

    }
#"batch_size" : 4
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    image_list=[]
    for num, i in enumerate(r['images']):
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('./static/'+filename +'_'+str(num)+'.png', pnginfo=pnginfo)
        image_list.append('./static/'+filename +'_'+str(num)+'.png')
    return image_list
