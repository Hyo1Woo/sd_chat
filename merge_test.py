from flask import Flask, render_template, request
from sd_api import stable_diffusion

#"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"

import os
import openai
openai.api_key = "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"
messages = []


app = Flask(__name__)


@app.route('/')
def home():
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

    result = f"The character is '{character}', set in the '{background}' background, approximately '{length}' words long, in the '{genre}' genre, and the story is '{story}'. An English level of '{english_level}' is suitable, and it's appropriate for a {age}-year-old."

    messages.append({"role": "user", "content": f"{result}"})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_content = completion.choices[0].message["content"].strip()
    messages.append({"role": "assistant", "content": f"{assistant_content}"})

    sentence = assistant_content.split('.')
    sentences = []
    for s in sentence:
        sentences.append(s.strip())

    for i , sent in enumerate(sentences[:-1]):
        prompt_make = "[sentence]: " + sent + "\n I'm going to draw a children's book with this sentence. I'm going to give a few words to the painter and have him paint a scene from one of the above. I hope the picture represents the above story well. Of course, even if the content isn't written in the story, if you think it's coherent, good for drawing, and good for conceiving a story that continues, you can create additional words to compose words. However, the more detailed the description, the better, but it should be concise. And when you reply to me, don't use other words, separate each set of words with ',' and pass it on. For example, 'brightness, a man who wears glasses and uses a computer, good-looking, Korean'."
        messages[-1] = {"role": "user", "content": f"{prompt_make}"}
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        prompt = 'fairy tale style, ' + completion.choices[0].message["content"].strip()
        #print(f"GPT : {assistant_content}")
        #sent.strip('\n')
        image_filename = str(i) + '_' + sent
        image_list = stable_diffusion(prompt=prompt, filename=image_filename)
        print(image_list)

    return render_template('result.html', result=assistant_content)


if __name__ == '__main__':
    app.run(debug=True)
