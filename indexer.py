from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Sample data
documents = ["Doc one text here", "Text of doc two", "Content of the third doc"]

# Create TF-IDF model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Save the model and matrix
with open('tfidf_model.pkl', 'wb') as f:
    pickle.dump((vectorizer, tfidf_matrix), f)

# Load the model and matrix
with open('tfidf_model.pkl', 'rb') as f:
    loaded_vectorizer, loaded_tfidf_matrix = pickle.load(f)

# Query processing
query = "doc text"
query_vector = loaded_vectorizer.transform([query])

# Calculate cosine similarity
cos_sim = cosine_similarity(query_vector, loaded_tfidf_matrix)

print("Cosine Similarity:", cos_sim)
