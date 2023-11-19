from flask import Flask, render_template, request, redirect, url_for, g
import openai
import PyPDF2
import os
import sqlite3
import hashlib

class PDFSummarizer:
    def __init__(self, database='summaries.db', openai_key=None):
        # Initialize Flask app and database configurations
        self.app = Flask(__name__)
        self.DATABASE = database
        openai.api_key = openai_key or os.getenv('OPENAI_API_KEY')
        self.bind_routes()  # Setup URL routes for the application

    def get_db(self):
        # Method to get the database connection
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE)
        return db

    def close_connection(self, exception):
        # Method to close the database connection
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def init_db(self):
        # Initialize the database by creating tables as per the schema
        with self.app.app_context():
            db = self.get_db()
            with self.app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    def extract_text_from_pdf(self, pdf_file):
        # TODO: Implement the method to extract text from a PDF file.
        # Use PyPDF2 to read the PDF file and extract text from each page.
        return "lots of pdf text"

    def openai_summarization(self, text):
        # TODO: Implement the method to use OpenAI for summarizing the text.
        # Use the OpenAI API to send the text and receive a summary.
        return "text summary grad"

    def bind_routes(self):
        # Define URL routes and their corresponding handlers

        @self.app.route('/', methods=['GET'])
        def index():
            # Render the file upload page
            return render_template('upload.html')

        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            # Handle file upload and process the PDF
            uploaded_file = request.files['file']
            if uploaded_file.filename == '':
                return redirect(url_for('index'))

            text = self.extract_text_from_pdf(uploaded_file)
            pdf_hash = hashlib.sha256(text.encode()).hexdigest()

            # TODO: Implement database caching logic.
            # Check for an existing summary in the database using the PDF's hash.
            # If it exists, use it. If not, generate a new summary, store it, and then use it.

            try:
                summary = self.openai_summarization(text)
                db = self.get_db()
                db.execute('INSERT INTO summaries (pdf_hash, summary) VALUES (?, ?)', (pdf_hash, summary))
                db.commit()
            except Exception as e:
                # Handle errors during summarization
                print(f"Error while summarizing: {e}")
                return "Error occurred during summarization.", 500

            return render_template('summary.html', summary=summary)

        @self.app.teardown_appcontext
        def close_connection(exception):
            # Ensure database connection is closed after request is complete
            self.close_connection(exception)

if __name__ == '__main__':
    # Run the Flask application
    app = PDFSummarizer()
    if not os.path.exists('summaries.db'):
        app.init_db()
    app.app.run(debug=True)


