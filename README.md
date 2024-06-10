# MultAI API Docker Initialization Guide

This guide provides instructions on how to set up and run the Docker container for the AI API which integrates various machine learning models for tasks such as chat, audio processing, vision, and image generation.

## Docker Setup

The Dockerfile provided sets up an environment based on NVIDIA CUDA for utilizing GPU capabilities essential for running AI models efficiently.

### Building the Docker Image

To build the Docker image, download this proyect, navigate to the directory and run the following command in your terminal:

```bash
docker build -t your_image_name .
```

Replace `your_image_name` with a name of your choice for the Docker image.

### Running the Docker Container

To run the Docker container, use the following command:

```bash
docker run --gpus all -d -p 5000:your_port --name your_container_name your_image_name
```

- `--gpus all` allows the Docker container to access all available GPUs.
- `-d` runs the container in detached mode.
- `-p 5000:your_port` maps the port 5000 inside the container used by the API to a port on your host machine. Replace `your_port` with the port number you wish to use.
- `--name your_container_name` sets a name for your running container.
- `your_image_name` is the name you specified when building the image.

### Custom Models Setup

The API downloads models from a specified [Google Drive folder](https://drive.google.com/drive/u/2/folders/12ZD7djHeHcwr4b1q7-5Te_AfGucl3627). You can customize which models to download by setting up your own Google Drive folder with the desired models, ensuring it follows the same structure as the one currently used.

#### Model Restrictions

- **Chat**: You can use any chat model as long as it is in the `.gguf` format.
- **Audio**: Currently, only Bark and Whisper models are supported.
- **Vision**: You can use any vision model available on [Hugging Face](https://huggingface.co/).
- **Images**: You are free to use any image generation model from [Hugging Face](https://huggingface.co/).

Ensure that the models you choose are compatible with the requirements and dependencies of the API.

To customize further the download of the models you can change the following command in the Dockerfile, making it be capable to download said models from somewhere else.
```Dockerfile
RUN gdown -q --folder "$DRIVE_LINK" -O /Api/
```
Make sure it downloads a folder named ModlFiles and that it follows the following estructure:
ModelFiles<br>
│<br>
├── Chat <br>
│ └── Model folders <br>
│ <br>
├── Images <br>
│ └── Model folders <br>
│ <br>
├── Vision <br>
│ └── Model folders <br>
│ <br>
└── Vision <br>
 └── Model folders<br>
 
And also that each model contains a .ini file with the same of the folder that contains the size of the model.

The new model will be adressed as the foldername of the model.

## Library
For easier use of this API and for migration from Openai's API take a look at our library [openMultAI](https://github.com/LiamMahmud/openMultAI)
## Conclusion

This setup allows to leverage powerful AI capabilities in their applications while maintaining control over the models and computational resources. By following these instructions, you can ensure that your AI API is ready to handle a wide range of tasks with efficiency and scalability.
