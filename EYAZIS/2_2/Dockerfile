FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download fr_core_news_sm
RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
    AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-fr'); \
    AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-en-fr')"
RUN python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('averaged_perceptron_tagger_eng', quiet=True); nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"

ENV TTS_MODEL_DIR=/app/tts_models
RUN mkdir -p /app/tts_models && \
    for v in fr_FR-siwis-medium fr_FR-tom-medium en_US-amy-medium en_US-lessac-medium; do \
        python3 -m piper.download_voices "$v" --data-dir /app/tts_models || exit 1; \
    done

ENV VOSK_MODEL_DIR=/app/vosk_models
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip && \
    mkdir -p /app/vosk_models && cd /tmp && \
    for v in vosk-model-small-en-us-0.15 vosk-model-small-fr-0.22; do \
        curl -fL -o "$v.zip" "https://alphacephei.com/vosk/models/$v.zip" && \
        unzip -q "$v.zip" -d /app/vosk_models && rm -f "$v.zip" || exit 1; \
    done && \
    rm -rf /var/lib/apt/lists/*

COPY backend/ .
COPY documents/ /app/documents/
COPY documents_fr/ /app/documents_fr/
COPY frontend/ /app/frontend/

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client espeak-ng && rm -rf /var/lib/apt/lists/*

COPY backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]
