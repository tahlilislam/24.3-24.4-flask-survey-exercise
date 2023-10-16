from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# Initialize responses as an empty list to store user answers
responses = []


@app.route('/')
def start_surver():
    """Select a survey."""

    return render_template("start_survey.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    return redirect("/questions/0")


@app.route('/questions/<int:q_id>')
def show_question(q_id):
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != q_id):
        # Trying to access questions out of order.
        flash(f"""Invalid question id: {q_id}. 
              Please answer the current question before moving on.""", "error")
        return redirect(f"/questions/{len(responses)}")

    # Get the current question from the survey
    current_question = survey.questions[q_id]

    return render_template("questions.html", ques_num=q_id+1, question=current_question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    final_choice = request.form["answer"]
    responses.append(final_choice)

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def survey_end():
    
    return render_template("survey_end.html")

