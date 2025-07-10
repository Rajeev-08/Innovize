import os
import json
import uuid
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime 


import google.generativeai as genai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.io as pio


import PyPDF2
from PIL import Image
import pytesseract


load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'supersecretkey'


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

USE_MOCK_AI = not GOOGLE_API_KEY
if USE_MOCK_AI:
    print("WARNING: Google API key not found. Running in MOCK mode.")

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)
IDEAS_FILE = 'data/ideas.json'


def load_ideas():
    if not os.path.exists(IDEAS_FILE): return []
    with open(IDEAS_FILE, 'r') as f:
        try: return json.load(f)
        except json.JSONDecodeError: return []
def save_ideas(ideas):
    with open(IDEAS_FILE, 'w') as f: json.dump(ideas, f, indent=2)
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages: text += page.extract_text() or ""
    except Exception as e: print(f"PDF Extraction Error: {e}")
    return text
def extract_text_from_image(file_path):
    try: return pytesseract.image_to_string(Image.open(file_path))
    except Exception as e: print(f"OCR Error: {e}"); return ""


def get_ai_evaluation(text):
    if USE_MOCK_AI:
        return {"technical_feasibility": {"score": 8, "reason": "Mock: Based on established technologies."}, "market_potential": {"score": 7, "reason": "Mock: Addresses a common pain point."}, "innovation_rating": {"score": 6, "reason": "Mock: Incremental improvement."}, "sustainability_relevance": {"score": 9, "reason": "Mock: Aligns with green initiatives."}, "strengths": "Mock: Clear value proposition.", "weaknesses": "Mock: Competitive space."}
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""Analyze the following business idea. Respond ONLY with a valid JSON object. The JSON must follow this exact structure: {{"technical_feasibility": {{"score": <1-10>, "reason": "<explanation>"}}, "market_potential": {{"score": <1-10>, "reason": "<explanation>"}}, "innovation_rating": {{"score": <1-10>, "reason": "<explanation>"}}, "sustainability_relevance": {{"score": <1-10>, "reason": "<explanation>"}}, "strengths": "<Summary of strengths>", "weaknesses": "<Summary of weaknesses>"}}. Idea Text:\n---\n{text}\n---"""
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Error calling Gemini for evaluation: {e}")
        return {"technical_feasibility": {"score": 0, "reason": "AI evaluation failed."}, "market_potential": {"score": 0, "reason": "AI evaluation failed."}, "innovation_rating": {"score": 0, "reason": "AI evaluation failed."}, "sustainability_relevance": {"score": 0, "reason": "AI evaluation failed."}, "strengths": "Could not generate AI analysis due to an API error.", "weaknesses": "Please check server logs and Google API key status."}
def get_ai_suggestions(text):
    if USE_MOCK_AI:
        return {"refined_title": "Mock: AI-Powered Customer Support Assistant", "improved_summary": "Mock: A concise summary focusing on key benefits.", "missing_components": ["Detailed revenue model", "Target user personas", "KPIs"]}
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"""You are a startup coach. Based on the following idea, provide concrete suggestions. Respond ONLY with a valid JSON object with this exact structure: {{"refined_title": "<A catchy and descriptive title>", "improved_summary": "<A rewritten, clearer summary>", "missing_components": ["<List of missing items like stakeholders, KPIs, etc.>"]}}. Idea Text:\n---\n{text}\n---"""
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Error calling Gemini for suggestions: {e}")
        return {"refined_title": "N/A - AI suggestion failed.", "improved_summary": "Could not generate AI suggestions due to an API error.", "missing_components": ["Please check your Google API key or account plan."]}

def generate_cluster_plot(ideas):
    if len(ideas) < 3: return None
    df = pd.DataFrame(ideas)
    df['description'] = df.get('description', '')
    df['text_for_clustering'] = df['title'] + " " + df['description']
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    X = vectorizer.fit_transform(df['text_for_clustering'])
    num_clusters = min(5, len(df.index) // 2); num_clusters = max(2, num_clusters)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto')
    df['cluster'] = kmeans.fit_predict(X.toarray())
    
    
    df['submission_time'] = pd.to_datetime(df['submission_time'])
    fig = px.scatter(df, x='submission_time', y='cluster', color='domain', hover_name='title',
                     hover_data={'description': True, 'cluster': False, 'submission_time': False},
                     title="Idea Clusters by Domain and Theme", labels={'submission_time': 'Submission Time', 'y': 'Thematic Cluster'})
    
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

def generate_summary_charts(ideas):
    if not ideas: return None
    df = pd.DataFrame(ideas)
    domain_counts = df['domain'].value_counts().reset_index()
    domain_counts.columns = ['domain', 'count']
    fig_domain = px.bar(domain_counts, x='domain', y='count', title='Ideas per Domain', text_auto=True)
    fig_domain.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return pio.to_html(fig_domain, full_html=False, include_plotlyjs='cdn')

# --- FLASK ROUTES ---
@app.route('/')
def index():
    ideas = load_ideas()
    cluster_plot_html = generate_cluster_plot(ideas)
    domain_chart_html = generate_summary_charts(ideas)
    return render_template('index.html', ideas=ideas, cluster_plot_html=cluster_plot_html, domain_chart_html=domain_chart_html)

@app.route('/submit', methods=['POST'])
def submit_idea():
    title = request.form.get('title')
    description = request.form.get('description')
    domain = request.form.get('domain')
    tags = request.form.get('tags')

    if not title or not description:
        flash("Title and Description are required.", "error")
        return redirect(url_for('index'))

    full_text = f"Title: {title}\nDescription: {description}"
    
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            extracted_text = ""
            if filename.lower().endswith('.pdf'): extracted_text = extract_text_from_pdf(filepath)
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')): extracted_text = extract_text_from_image(filepath)
            if extracted_text: full_text += f"\n\n--- Extracted Text from Attachment ---\n{extracted_text}"
            os.remove(filepath)

    ai_evaluation = get_ai_evaluation(full_text)
    ai_suggestions = get_ai_suggestions(full_text)

    new_idea = {
        'id': f"idea_{uuid.uuid4().hex}",
        'title': title, 'description': description, 'domain': domain,
        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()] if tags else [],
        'full_text': full_text, 'ai_evaluation': ai_evaluation, 'ai_suggestions': ai_suggestions,
        'submission_time': datetime.now().isoformat()  
    }

    ideas = load_ideas(); ideas.insert(0, new_idea); save_ideas(ideas)
    flash("Your idea has been successfully submitted and analyzed!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)