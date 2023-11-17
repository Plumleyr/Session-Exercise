from flask import Flask, render_template, redirect, request, url_for, flash

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey, Survey, Question

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zzz'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/', methods = ['POST', 'GET'])
def show_survey():
    if request.method == 'POST':
        return redirect(url_for('show_questions', question_number = 0))

    return render_template('survey.html', satisfaction_survey = satisfaction_survey)

@app.route('/question/<int:question_number>', methods = ['POST', 'GET'])
def show_questions(question_number=0):
    if question_number != len(responses):
        flash("Invalid link, redirected to correct question.")
        return redirect(url_for('show_questions', question_number = len(responses)))
    else:
        return render_template('questions.html', question_number = question_number, satisfaction_survey = satisfaction_survey)

@app.route('/thank_you')
def show_thanks():
    return render_template('thank_you.html')

@app.route('/answer', methods = ['POST', 'GET'])
def show_answers():
    responses.append(request.form['choice'])
    question_number = int(request.args.get('question_number')) + 1
    if question_number < len(satisfaction_survey.questions):
        return redirect(url_for('show_questions', question_number = question_number))
    else:
        return redirect('/thank_you')

