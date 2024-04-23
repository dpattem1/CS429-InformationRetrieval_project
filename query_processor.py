import nltk
nltk.download('popular')

from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import wordnet as wn

app = Flask(__name__)

# Documents pulled from the provided URL
documents = [
    "A hyperlink points to a whole document or to a specific element within a document.",
    "Hypertext is text with hyperlinks.",
    "A software system that is used for viewing and creating hypertext is a hypertext system.",
    "There can be a hypertext link to any piece of text."
]

# Vectorizer and TF-IDF model setup
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

def get_synonyms(word):
    """Get synonyms from WordNet and return a single string"""
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    # Return a single string instead of a list
    return ' '.join(synonyms)


def correct_spelling(word):
    """Simple spelling correction implementation using NLTK"""
    from nltk.corpus import words
    correct_words = words.words()
    # Placeholder for a more complex algorithm
    return word if word in correct_words else None

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        json_data = request.get_json()
        query = json_data.get('query')
        k = json_data.get('top_k', 5)  # Default to Top-5 results

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Query expansion (optional)
        query_expanded = ' '.join(get_synonyms(word) for word in query.split())

        # Process the query
        query_tfidf = vectorizer.transform([query_expanded])
        cos_sim = cosine_similarity(query_tfidf, tfidf_matrix)

        # Get top K results
        top_indices = cos_sim.argsort()[0][-k:][::-1]
        results = [{'document': documents[idx], 'score': cos_sim[0, idx]} for idx in top_indices]

        return jsonify(results), 200

    elif request.method == 'GET':
        # GET method is not suitable for this operation
        return jsonify({'message': 'GET method is not implemented for search. Use POST instead.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
