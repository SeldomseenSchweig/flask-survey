from dis import Instruction
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey

# satisfaction_survey = Survey(
#     "Customer Satisfaction Survey",
#     "Please fill out a survey about your experience with us.",
#     [
#         Question("Have you shopped here before?"),
#         Question("Did someone else shop with you today?"),
#         Question("On average, how much do you spend a month on frisbees?",
#                  ["Less than $10,000", "$10,000 or more"]),
#         Question("Are you likely to shop here again?"),
#     ])

responses = []
number = 0

app = Flask(__name__)

app.config['SECRET_KEY'] = "hayduke"

debug = DebugToolbarExtension(app)


@app.route('/')
def introduce_survey():
    """" This will be the first page and introduce the survey """
    title = satisfaction_survey.title 
    instructions = satisfaction_survey.instructions

    return render_template('home.html', title = title, instructions = instructions)

@app.route('/question/<number>')
def question(number):
    number =  int(number)
    """This is a question template that will be reused for each question"""
    question = satisfaction_survey.questions[number].question
    options = satisfaction_survey.questions[number].choices
    return render_template('question.html', question= question, options= options, number = number)

@app.route('/answer', methods=["POST"])
def add_response():

    """This will send the answer to the response list and 
    redirect to next question, with a flash"""
    answer = request.form['answer']
    print("hello - " + answer)
    responses.append(answer)
    return redirect("/question/3")
