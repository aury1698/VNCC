FROM ubuntu:latest

# Install necessary packages
RUN apt-get -q update -y && \
    apt-get -q install -y \
    apt-transport-https \
    apt-utils \
    build-essential \
    cron \
    curl \
    g++ \
    git \
    gcc \
    libcairo2-dev \
    libexpat1 \
    libffi-dev \
    libssl-dev \
    libx11-dev \
    libxml2-dev \
    libxslt1-dev \
    libxss1 \
    nano \
    netcat-traditional \
    pango1.0-tests \
    psmisc \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    ssl-cert \
    vim \
    zlib1g \
    zlib1g-dev

# Create a non-root user
WORKDIR /home/app/
RUN useradd -m appuser
RUN chown -R appuser:appuser /home/app
USER appuser

# Set up the working directory and copy application files
WORKDIR /home/app/
COPY index.py .
COPY requirements.txt .
COPY model.pkl .

# Set environment variables for Python paths
ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python:/home/app/function

# Install Python dependencies
RUN python3 -m venv test
RUN test/bin/pip3 install --no-cache-dir -r requirements.txt

WORKDIR /home/app/
USER appuser

EXPOSE 6001
CMD ["test/bin/python3", "index.py"]