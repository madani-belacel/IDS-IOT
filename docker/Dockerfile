# RPL-ClusterIDS — Ubuntu 22.04 toolchain for Cooja campaigns
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CONTIKI_NG=/opt/contiki-ng
ENV IDS_ROOT=/workspace/IDS_IOT
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ant \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    python3-venv \
    gcc-arm-none-eabi \
    lib32z1 \
    curl \
    wget \
    ca-certificates \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-bibtex-extra \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch release/v4.8 https://github.com/contiki-ng/contiki-ng.git ${CONTIKI_NG}

WORKDIR ${IDS_ROOT}

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt

# Project mounted at runtime: docker compose run campaign
CMD ["/bin/bash"]
