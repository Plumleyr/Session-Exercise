from flask import Flask, render_template, redirect, request, url_for, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys_set, satisfaction_survey, personality_quiz, Survey, Question

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zzz'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.route('/')
def pick_survey():
    return render_template('pick_a_survey.html', surveys_set = surveys_set)

@app.route('/survey',  methods = ['GET', 'POST'])
def show_survey():
    survey_name = request.args['selected_survey']
    selected_survey = surveys_set[survey_name]
    session['responses'] = []
    session['survey_name'] = survey_name
    return render_template('survey.html', selected_survey = selected_survey, survey_name = survey_name)

@app.route('/question/<int:question_number>', methods = ['POST', 'GET'])
def show_questions(question_number=0):
    if question_number != len(session['responses']):
        flash("Invalid link, redirected to correct question.")
        return redirect(url_for('show_questions', question_number = len(session['responses'])))
    elif len(session['responses']) == len(surveys_set[session['survey_name']].questions):
        return redirect('/thank_you')
    else:
        return render_template('questions.html', question_number = question_number, surveys_set = surveys_set)

@app.route('/thank_you')
def show_thanks():
    return render_template('thank_you.html')

@app.route('/answer', methods = ['POST', 'GET'])
def show_answers():
    if len(session['responses']) < len(surveys_set[session['survey_name']].questions) and len(session['responses']) == int(request.args.get('question_number')):
        responses = session['responses']
        responses.append(request.form['choice'])
        session['responses'] = responses
        question_number = int(request.args.get('question_number')) + 1
        if question_number < len(surveys_set[session['survey_name']].questions):
            return redirect(url_for('show_questions', question_number = question_number))
        else:
            return redirect('/thank_you')
    else:
        return redirect(url_for('show_questions', question_number = len(session['responses'])))


