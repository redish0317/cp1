from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')