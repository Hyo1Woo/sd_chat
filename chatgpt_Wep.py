from flask import Flask, render_template, request

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
    #print(f"GPT : {assistant_content}")

    return render_template('result.html', result=assistant_content)


if __name__ == '__main__':
    app.run(debug=True)