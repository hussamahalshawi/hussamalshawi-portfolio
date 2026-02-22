from flask import Blueprint, render_template

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/')
def index():
    dummy_projects = [
        {
            'title': 'AI Chatbot',
            'desc': 'Python & NLP project',
            'image': 'p1.jpg'
        },
        {
            'title': 'Portfolio Site',
            'desc': 'Flask & Tailwind project',
            'image': 'p2.jpg'
        }
    ]
    return render_template('index.html', projects=dummy_projects)