# Object-Detection-Pytorch-YoloV5

## Instructions for how to use this repository
First make sure you have git installed on your device and clone this project

# Installing Python
Python version >= 3.8 required
Download from here : 
```
https://www.python.org/downloads/
```
Be sure to add python installation directory to Path in Environment Variables
Python already comes with pip package manager which is good

# Creating Virtual Environment
This step is optional you don’t need to create a virtual environment but it is recommended to create one. Virtual environment is useful for isolating project packages and dependencies from each other. So create a virtual environment in the same directory that you cloned this project.
First open command line on windows and change directory to the cloned folder then execute the following command which will create a virtual environment :
```
Python -m venv  VirtualEnvironment
```
Then activate the virtual environment before proceeding to next step:
```
	Python virutalEnvironment\Scripts\activate
```

# Installing Pytorch
This setup will automatically download Cuda 11.3 and cudnn
For GPU Cuda based computation:
```
pip3 install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```
For CPU based computations:
```
	pip3 install torch torchvision torchaudio
```

# Installing Yolov5
Make sure that you are in your cloned project directory then execute this git command
```
	git clone https://github.com/ultralytics/yolov5
```
Then execute this command to install dependencies:
```
cd yolov5 && pip install -r requirements.txt
```


