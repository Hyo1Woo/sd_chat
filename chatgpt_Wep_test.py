from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        english_level = request.form["english_level"]
        age = request.form["age"]
        character = request.form["character"]
        background = request.form["background"]
        genre = request.form["genre"]
        length = request.form["length"]
        story = request.form["story"]

        result = f"The character is '{character}', set in the '{background}' background, approximately '{length}' words long, in the '{genre}' genre, and the story is '{story}'. An English level of '{english_level}' is suitable, and it's appropriate for a {age}-year-old."
        return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
