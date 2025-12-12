from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "69"   # Required for sessions


@app.route("/")
def randomheadline():
    con = sqlite3.connect("fakeNewsUpdated.db")
    # Select the headline and the realOrFake column explicitly so we know indices
    test = con.execute("SELECT content, realOrFake FROM FakeNews").fetchall()
    con.close()

    # Choose one headline at random
    headline = random.choice(test)
    headline_text = headline[0]
    headline_label = headline[1] 

    session["correct_answer"] = headline_label
    session["headline"] = headline_text

    # Initialize score in session if not present
    if "score" not in session:
        session["score"] = 0

    return render_template("index.html", headline=headline_text, result=None, score=session.get("score", 0))


@app.route("/check", methods=["POST"])
def check():
    user_answer = request.form.get("answer")  # could be 'true'/'false' or 'real'/'fake'
    correct_answer = session.get("correct_answer")

    def to_bool(val):
        if isinstance(val, bool):
            return val
        if val is None:
            return False
        s = str(val).strip().lower()
        return s in ("1", "true", "t", "yes", "y", "real", "r")

    user_bool = to_bool(user_answer)
    correct_bool = to_bool(correct_answer)

    if user_bool == correct_bool:
        result = "Correct!"
        # increment score when correct
        session["score"] = session.get("score", 0) + 1
    else:
        result = "Incorrect!"

    return render_template("index.html", headline=session.get("headline"), result=result, score=session.get("score", 0))


@app.route("/reset", methods=["POST"])
def reset():
    session["score"] = 0
    return redirect(url_for("randomheadline"))


if __name__ == "__main__":
    app.run(debug=True)
