FROM nvidia/cuda:12.5.0-base-ubuntu22.04

ARG DRIVE_LINK=https://drive.google.com/drive/u/2/folders/12ZD7djHeHcwr4b1q7-5Te_AfGucl3627

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    git \
    ca-certificates \
    build-essential \
    dpkg \
    lsb-release \
    gnupg \
    nano \
    vim \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt-get update

RUN apt-get -y install  cuda-toolkit-12-5


RUN apt-get install ffmpeg -y


RUN pip3 install flask accelerate transformers soundfile requests regex pillow openai-whisper bitsandbytes scipy uuid pynvml psutil zipstream-new diffusers gdown

RUN pip3 install --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN CMAKE_ARGS="-DLLAMA_CUDA=on" pip3 install llama-cpp-python

EXPOSE 5000

RUN mkdir -p /Api

RUN git clone https://github.com/LiamMahmud/MultAI /Api

RUN gdown -q --folder "$DRIVE_LINK" -O /Api/

WORKDIR /Api

CMD ["python3", "API.py"]

