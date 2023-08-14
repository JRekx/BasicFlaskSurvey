from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# Key names will store itemes in sessions.

RESPONSE_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "RosaLockOut"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Selects a survey"""

    return render_template("survey_start.html",survey=survey)

@app.route("/begin",methods =["POST"])
def survey_start():
    """Clear respones in sessions"""

    session[RESPONSE_KEY] = []

    return redirect("/questions/0")

@app.route("/answer",methods =["POST"])
def handle_question():
    """Saves the response and directs to the next question"""

    choice = request.form['answer']
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Display current questions"""
    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect("/")
    # trys to access question page to soon

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    # amswerd all the questions!

    if (len(responses) != qid):
        flash(f"INVALID QUESTION ID:{qid}.")
        return redirect (f"/questions/{len(responses)}")
    # trying to access questions of order!!

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app. route("/complete")
def complete():
    """SURVEY IS DONE! PROMPT NEW PAGE"""

    return render_template("complete.html")