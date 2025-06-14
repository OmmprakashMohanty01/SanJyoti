from flask import Blueprint, render_template, request, redirect
import subprocess
import random
import PyPDF2

main = Blueprint('main', __name__)

def generate_quiz(topic):
    sample_questions = [
        f"Explain the basic concept of {topic}.",
        f"State one key point about {topic}.",
        f"List an advantage or disadvantage of {topic}.",
        f"Why is {topic} important?",
        f"Give real-life examples related to {topic}."
    ]
    return random.sample(sample_questions, min(5, len(sample_questions)))

@main.route('/', methods=['GET', 'POST'])
def index():
    explanation = ''
    quiz_questions = []
    summary = ''
    pdf_quiz = []

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'explain':
            topic = request.form['topic']
            prompt = f"Explain the following topic in detail: {topic}"
            try:
                result = subprocess.run(['ollama', 'run', 'llama3', prompt], capture_output=True, text=True, timeout=300)
                explanation = result.stdout.strip()
            except Exception as e:
                explanation = f"Error generating explanation: {e}"

        elif action == 'quiz':
            topic = request.form['topic']
            quiz_questions = generate_quiz(topic)

        elif action == 'google':
            topic = request.form['topic']
            return redirect(f"https://www.google.com/search?q={topic}")

        elif action == 'upload':
            file = request.files['pdf_file']
            if file:
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text

                    summary_prompt = f"Summarize the following PDF content:\n{text[:3000]}"
                    result = subprocess.run(['ollama', 'run', 'llama3', summary_prompt], capture_output=True, text=True, timeout=300)
                    summary = result.stdout.strip()

                    pdf_quiz = generate_quiz('the provided PDF')

                except Exception as e:
                    summary = f"Error processing PDF: {e}"

    # ✅ Always return a response in every case
    return render_template('index.html', explanation=explanation, quiz_questions=quiz_questions, summary=summary, pdf_quiz=pdf_quiz)
