from flask import Flask, render_template, request, jsonify
from dynamic_scraper import dynamic_scrape
from deepfake_detection import analyze_media

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/analyze_profile', methods=['POST'])
def analyze_profile():
    try:
        url = request.form['profile_url']
        # Dynamic scraping for the URL
        scraped_data = dynamic_scrape(url)

        # Add suspicion score logic
        suspicion_scores = {}

        # Analyzing text (bio)
        if 'paragraphs' in scraped_data:
            for paragraph in scraped_data['paragraphs']:
                if is_suspicious_bio(paragraph):
                    suspicion_scores['bio'] = 0.9  # High suspicion
                else:
                    suspicion_scores['bio'] = 0.1  # Low suspicion
        
        # Analyze images for deepfakes
        if 'images' in scraped_data:
            deepfake_results = analyze_media(scraped_data['images'])
            scraped_data['deepfake_results'] = deepfake_results

            # Assign higher suspicion score if deepfakes are detected
            suspicion_scores['images'] = 0.8 if any('Deepfake detected' in result for result in deepfake_results.values()) else 0.2

        scraped_data['suspicion_scores'] = suspicion_scores
        return jsonify({'status': 'success', 'data': scraped_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def is_suspicious_bio(bio):
    # Placeholder logic for detecting suspicious bio content
    suspicious_keywords = ['fake', 'scam', 'unverified']
    return any(keyword in bio.lower() for keyword in suspicious_keywords)

if __name__ == '__main__':
    app.run(debug=True)
