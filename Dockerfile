# Use an official NVIDIA CUDA base image with CUDA and cuDNN
FROM nvidia/cuda:12.3.0-base-ubuntu22.04

# Set non-interactive installation mode
ARG DEBIAN_FRONTEND=noninteractive

# Install essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    git \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
#ENV MINICONDA_VERSION=py39_4.9.2
#RUN wget https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O /tmp/miniconda.sh \
#    && bash /tmp/miniconda.sh -b -p /opt/conda \
#    && rm /tmp/miniconda.sh

# Add Conda to PATH
ENV PATH=/opt/conda/bin:${PATH}

# Create a Conda environment
#RUN conda create -n myenv python=3.8.19
# Activate the Conda environment
#SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY ./Tests/Llama-7b.py ./ModelFiles/Llama2-7b/llama-2-7b-chat.Q5_K_M.gguf ./

# Install any additional packages
#RUN conda install numpy pandas scikit-learn matplotlib

# Set the default command to Python3
#CMD ["conda", "run", "-n", "myenv", "python"]
