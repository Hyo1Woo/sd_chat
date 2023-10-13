from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from sd_api import stable_diffusion
import shutil
#"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"
import re

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



def extract_number_from_filename(image_list):
    match = re.search(r'\d+', image_list)
    return int(match.group()) if match else -1

import os
import openai
openai.api_key = "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"
messages = []
app = Flask(__name__)


@app.route('/')
def home():
    os.system("rm -rf ./temp/*")
    os.system("rm -rf ./static/*")
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    english_level = request.form['english_level']
    age = request.form['age']
    character = request.form['character']
    background = request.form['background']
    genre = request.form['genre']
    length = request.form['length']
    story = request.form['story']

    if int(length) > 500:
        length = '500'

    result = f"The character is '{character}', set in the '{background}' background, approximately '{length}' words long, in the '{genre}' genre, and the story is '{story}'. An English level of '{english_level}' is suitable, and it's appropriate for a {age}-year-old."

    messages.append({"role": "user", "content": f"{result}"})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_content = completion.choices[0].message["content"].strip()
    messages.append({"role": "assistant", "content": f"{assistant_content}"})

    return render_template('result.html', result=assistant_content)





@app.route('/next_page')
def next_page():
    assistant_content = request.args.get('assistant_content', '')
    sentence = assistant_content.split('.')
    sentences = []
    for s in sentence:
        sentences.append(s.strip())
    image_book=[]
    for i, sent in enumerate(sentences[:-1]):
        prompt_make = "[sentence]: " + sent + "\n I'm going to draw a children's book with this sentence. I'm going to give a few words to the painter and have him paint a scene from one of the above. I hope the picture represents the above story well. Of course, even if the content isn't written in the story, if you think it's coherent, good for drawing, and good for conceiving a story that continues, you can create additional words to compose words. However, the more detailed the description, the better, but it should be concise. And when you reply to me, don't use other words, separate each set of words with ',' and pass it on. For example, 'brightness, a man who wears glasses and uses a computer, good-looking, Korean'."
        messages[-1] = {"role": "user", "content": f"{prompt_make}"}
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        prompt = 'fairy tale style, ' + completion.choices[0].message["content"].strip()
        # print(f"GPT : {assistant_content}")
        # sent.strip('\n')
        image_filename = str(i) + '_' + sent
        image_list = stable_diffusion(prompt=prompt, filename=image_filename)
        print(image_list)
        image_book.extend(image_list)
    return render_template('next_page.html', image_list=image_book)


@app.route('/submit', methods=['POST'])
def submit():
    argument = request.args.get('argument', '')
    return redirect(url_for('next_page', assistant_content=argument))


@app.route('/done', methods=['POST'])
def done():
    return redirect(url_for('final'))


folder_path = "./static"
@app.route("/save-image", methods=["POST"])
def save_image():
    image_name = request.json["name"]
    source_path = os.path.join(folder_path, image_name)
    save_path = os.path.join("temp", image_name)
    if not os.path.exists("temp"):
        os.makedirs("temp")

    shutil.copy(source_path, save_path)

    return "", 200

temp_folder_path = './temp'
@app.route("/final")
def final():
    temp_image_list = get_image_paths(temp_folder_path)
    temp_image_list = sorted(temp_image_list, key=extract_number_from_filename)
    temp_image_name = []
    for path in temp_image_list:
        #s = path.split('/')
        temp_image_name.append('./static'+path[6:])

    return render_template('final.html', temp_image_list=temp_image_name)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
