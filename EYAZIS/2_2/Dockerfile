FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install  -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
    AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-fr'); \
    AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-en-fr')"
RUN python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('averaged_perceptron_tagger_eng', quiet=True); nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"

COPY backend/ .
COPY documents/ /app/documents/
COPY documents_fr/ /app/documents_fr/
COPY frontend/ /app/frontend/

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

COPY backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]
