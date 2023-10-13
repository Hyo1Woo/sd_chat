import os
import shutil
from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

def get_image_paths(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_list = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in image_extensions:
                image_list.append(file_path)

    return image_list

import re

folder_path = "./static"
image_list = get_image_paths(folder_path)
def extract_number_from_filename(image_list):
    match = re.search(r'\d+', image_list)
    return int(match.group()) if match else -1

image_list = sorted(image_list, key=extract_number_from_filename)

@app.route("/")
def display_images():
    return render_template_string("""
        <!doctype html>
        <html>
            <head>
                <title>이미지 리스트</title>
                <style>
                    .image-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                        grid-gap: 10px;
                        justify-items: center;
                        align-items: center;
                    }
                    img {
                        width: 100%;
                        height: auto;
                        max-width: 200px;
                        cursor: pointer;
                    }
                    figcaption {
                        text-align: center;
                        font-size: 14px;
                        margin-top: 5px;
                    }
                </style>
                <script>
                    function saveImage(imageName, clickedImage) {
                        fetch('/save-image', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ name: imageName })
                        }).then(response => {
                            if (response.ok) {
                                alert('이미지가 저장되었습니다.');
                                clickedImage.style.border = "5px solid red";
                            } else {
                                alert('이미지 저장에 실패했습니다.');
                            }
                        });
                    }
                </script>
            </head>
            <body>
                <div class="image-grid">
                    {% for image in image_list %}
                        <figure>
                            <img src="{{ image }}" alt="{{ image }}" onclick="saveImage('{{ image.split('/')[-1] }}', this)">
                            <figcaption>{{ image.split('/')[-1] }}</figcaption>
                        </figure>
                    {% endfor %}
                </div>
            </body>
        </html>
    """, image_list=image_list)


@app.route("/save-image", methods=["POST"])
def save_image():
    image_name = request.json["name"]
    source_path = os.path.join(folder_path, image_name)
    save_path = os.path.join("temp", image_name)

    if not os.path.exists("temp"):
        os.makedirs("temp")

    shutil.copy(source_path, save_path)

    return "", 200

if __name__ == "__main__":
    app.run(debug=True)