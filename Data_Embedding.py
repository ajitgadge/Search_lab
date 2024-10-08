=====Embedding the data for semantic search and Hybrid Search =====================


import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

# Load the model. Use General LLM model 'allMiniLM-L6-v2' for simple text
model = SentenceTransformer('all-MiniLM-L6-v2')

# Establish the connection to the PostgreSQL database
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)
cursor = conn.cursor()

# Fetch the data from the body column
cursor.execute("SELECT id, body FROM articles WHERE embeddings IS NULL")
articles = cursor.fetchall()

# Prepare and execute the update queries
for article in articles:
    article_id, body_text = article
    # Generate the embedding
    embedding = model.encode(body_text).tolist()
    # Update the embedding column in the database
    cursor.execute(
        "UPDATE articles SET embeddings = %s WHERE id = %s",
        (embedding, article_id)
    )

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"Updated  articles with embeddings.")

