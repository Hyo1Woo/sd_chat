import os
import shutil
from flask import Flask, render_template_string, request, redirect, url_for
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

folder_path = "./static"
temp_folder_path = "./temp"
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
                <title>Image list</title>
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
                    #done-button {
                        display: block;
                        margin: 20px auto;
                        padding: 10px;
                        background-color: blue;
                        color: white;
                        text-align: center;
                        cursor: pointer;
                        width: 100px;
                        text-decoration: none;
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <div class="image-grid">
                    {% for image in image_list %}
                        <figure>
                            <img src="{{ image }}" alt="{{ image }}">
                            <figcaption>{{ image. split('/')[-1] }}</figcaption>
                        </figure>
                    {% endfor %}
                </div>
                <a href="{{ url_for('display_temp_images') }}" id="done-button">Done</a>
            </body>
        </html>
    """, image_list=image_list)

@app.route("/temp")
def display_temp_images():
    temp_image_list = get_image_paths(temp_folder_path)
    temp_image_list = sorted(temp_image_list, key=extract_number_from_filename)

    return render_template_string("""
        <!doctype html>
        <html>
            <head>
                <title>Temp Image list</title>
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
            </head>
            <body>
                <div class="image-grid">
                    {% for image in temp_image_list %}
                        <figure>
                            <img src="{{ image }}" alt="{{ image }}">
                            <figcaption>{{ image. split('/')[-1] }}</figcaption>
                        </figure>
                    {% endfor %}
                </div>
            </body>
        </html>
    """, temp_image_list=temp_image_list)

if __name__ == "__main__":
    app.run(debug=True)

