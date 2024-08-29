# NON UTILIZZARE, TEST
# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements.txt e handler.py nella directory di lavoro
COPY requirements.txt .
COPY handler.py .
COPY /path/to/model.pkl ./model.pkl

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Imposta il comando di avvio
CMD ["python", "handler.py"]