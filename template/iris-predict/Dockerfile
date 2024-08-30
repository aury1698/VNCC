# Step 2: Use a more recent Ubuntu version as the base for the main image and import the watchdog image
ARG PYTHON_VERSION=3
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/classic-watchdog:0.3.1 AS watchdog
FROM ubuntu:latest

ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Step 3: Install necessary packages
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

# Step 4: Copy fwatchdog from the watchdog image
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Step 5: Create a non-root user (optional, but recommended)
WORKDIR /home/app/
RUN useradd -m appuser
RUN chown -R appuser:appuser /home/app
USER appuser

# Step 6: Set up the working directory and copy application files
WORKDIR /home/app/
COPY index.py .
COPY requirements.txt .
COPY model.pkl .
#COPY handler.py .

# Step 7: Set environment variables for Python paths
ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python:/home/app/function

# Step 8: Install Python dependencies
RUN python3 -m venv test
RUN test/bin/pip3 install --no-cache-dir -r requirements.txt
#RUN pip3 install --user -r requirements.txt
#RUN . test/bin/activate

# Step 9: Set up the function directory
RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt .
#RUN test/bin/pip3 install --user -r requirements.txt
RUN ../test/bin/pip3 install --no-cache-dir -r requirements.txt
#RUN pip3 install --user -r requirements.txt

WORKDIR /home/app/
USER root
COPY function function
USER appuser

# Step 10: Set the environment variables for the watchdog and expose the port
ENV fprocess="test/bin/python3 /home/app/index.py"
ENV write_timeout=300s
EXPOSE 8080

# Step 11: Add a health check and specify the command to start the function
HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1
CMD ["fwatchdog"]
