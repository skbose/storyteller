#Using the base image with Python 3.10
FROM nvidia/cuda:12.2.0-devel-ubuntu20.04

WORKDIR /

# Install git, wget, build-essential
RUN apt-get update && apt-get install -y git wget build-essential

RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz && \
    tar xvf ffmpeg-git-amd64-static.tar.xz
ENV PATH="/ffmpeg-git-20230915-amd64-static:${PATH}"

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/miniconda/bin:${PATH}"

# change workdir inside app
WORKDIR /main

# Create the Conda environment
RUN conda create -n fables python=3.10 && \
    echo "source activate fables" > ~/.bashrc
ENV PATH /miniconda/envs/fables/bin:$PATH

# Set the shell for the following commands to use the Conda environment "ttts-fast"
SHELL ["conda", "run", "-n", "fables", "/bin/bash", "-c"]

ENV FLASK_APP=main/app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#Exposing port 5000 from the container
EXPOSE 5000

COPY . .

#Starting the Python application
CMD ["flask", "run"]
