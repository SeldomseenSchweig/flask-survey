from dis import Instruction
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey


responses = []
page = 0

app = Flask(__name__)

app.config['SECRET_KEY'] = "hayduke"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

debug = DebugToolbarExtension(app)


@app.route('/')
def introduce_survey():
    """" This will be the first page and introduce the survey """
    title = satisfaction_survey.title 
    instructions = satisfaction_survey.instructions

    return render_template('home.html', title = title, instructions = instructions)

@app.route('/question/<number>')
def question(number):
    """This is a question template that will be reused for each question"""
    number =  int(number)

    """ This checks if the user is trying to 
    put in a question they shouldn't access 
    it will send them to the Q that they are on"""

    

    # if not number == len(responses):
    #     flash("You tried to access a question out of order", 'error')
    #     new_page = ""
    #     new_page =  "/question/" + str(len(responses))
    #     return redirect(new_page)
    # elif len(satisfaction_survey.questions) == len(responses):
    #     flash("You have already completed the survey!", 'error')   
    #     return redirect('/end_of_survey')

    if  len(satisfaction_survey.questions) == len(responses):
        flash("You have already completed the survey!", 'error')
        new_page = ""
        new_page =  "/question/" + str(len(responses))
        return redirect('/end_of_survey')
    elif not number == len(responses):
        flash("You tried to access a question out of order", 'error')    
        return redirect(new_page)


    question = satisfaction_survey.questions[number].question
    options = satisfaction_survey.questions[number].choices
    return render_template('question.html', question= question, options= options, number = number)

@app.route('/answer', methods=["POST"])
def add_response():
    new_page = ""
    """This will send the answer to the response list and 
    redirect to next question or to the end of the survey Thank You page, with a flash"""
    answer = request.form['response']
    responses.append(answer)
    new_page =  "/question/" + str(len(responses))
    
    if len(satisfaction_survey.questions) == len(responses):      
        return redirect('/end_of_survey')
    else:
        return redirect(new_page)

@app.route('/end_of_survey')
def end_of_survey():
        return render_template('thank_you.html')


