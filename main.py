"""
Command line utility to read in specified html file and parse out all the quiz questions and answer choices, then save
it as json.
"""

import argparse
import json
import os
from pprint import pprint

from bs4 import BeautifulSoup


def parse_quiz_html(html_file):
    '''
    Parse the quiz html file and return a dictionary of questions and answer choices.

    Example question structure:
    /html/body/div[@id='application']/div[@id='wrapper']/div[@id='main']/div/div[@id='content-wrapper']/div/div/div[2]/div[@id='questions']/div[@id='']/div[@id='question_6356789']/div[5]/div[1]/textarea[@name='question_text']
    '''
    with open(html_file, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    questions = {}

    # Find div with id 'questions'
    questions_div = soup.find('div', id='questions')

    # Find all divs with id 'question_'
    question_divs = questions_div.find_all('div', id=lambda x: x and x.startswith('question_'))

    # Loop through each question div
    for question_div in question_divs:
        # Structure:
        # /div[5]/div[1]/textarea[@name='question_text']

        # Get div with class 'original_question_text'
        original_question_text_div = question_div.find('div', attrs={'class': 'original_question_text'})

        if original_question_text_div is None:
            continue

        # Get the question text
        question_text = original_question_text_div.find('textarea',
                                                        attrs={'class': 'textarea_question_text'}).text.strip()
        question_text = question_text.replace('<br>', '')

        # Remove all whitespace from question text except for single spaces
        question_text = ' '.join(question_text.split())

        # Get question id
        question_id = question_div['id'].split('_')[1]

        # Add question to questions dict
        questions[question_id] = {
            'question': question_text,
            'answers': []
        }

    # Get div with answers from questions div with id 'answer_'
    answer_divs = questions_div.find_all('div', id=lambda x: x and x.startswith('answer_'))

    # Loop through each answer div
    for answer_div in answer_divs:
        # Get answer text from div with class 'answer_text'
        answer_text = answer_div.find('div', attrs={'class': 'answer_text'}).text.strip()

        # Remove all whitespace from answer text except for single spaces
        answer_text = ' '.join(answer_text.split())

        selected = 'selected_answer' in answer_div['class']

        # Get the corresponding question id from the input name
        question_id = \
            answer_div.find('input', attrs={'name': lambda x: x and x.startswith('question-')})['name'].split('-')[1]

        # Add answer text to questions dict
        questions[question_id]['answers'].append(answer_text)

        if selected:
            questions[question_id]['correct'] = answer_text

    return questions


def save_questions(questions, output_file):
    '''
    Save the questions to the specified output file.
    '''

    # Create output directory if it doesn't exist
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(output_file, 'w') as f:
        json.dump(questions, f)


# Parse command line arguments
parser = argparse.ArgumentParser(description='Parse quiz html file and save as json.')
parser.add_argument('html_file', help='Path to the html file to parse.')

# Add arg for output file name, default to the same name as the html file ending in .json instead of .html
# in the subdirectory 'output'

args = parser.parse_args()
parser.add_argument('-o', '--output', default='output/{}.json'.format(args.html_file.split('/')[-1].split('.')[0]),
                    help='Path to the output file.')

args = parser.parse_args()

# Parse the html file
questions = parse_quiz_html(args.html_file)

questions = list(questions.values())

# Save the questions
save_questions(questions, args.output)
