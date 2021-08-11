# SEALNET

This document is intended as a detailed guide to help with
installation and running of
SealNet, a face recognition software for Harbor Seals. The
instructions are intended to
run the software on Amazon Web Services (AWS) EC2 cluster running
Linux but they can be
modified for use on other setups running Linux or other Unix-like
systems.
To run a command, type it out on the terminal and hit enter.

# Prerequisite

To run this program we need python 3.7 installed. You can check your python version
by typing `python3 -V`. If you don't have python 3.7, you can download it here:
https://www.python.org/downloads/release/python-379/.

If you are using the AWS cluster, it is already installed for you.

# Data

SealNet is a face recognition software that is trained using photos.
As of now, the software
expects files of png, jpg and jpeg formats.
The directories must be structured as follows:
```
.
├── SealFaceRecognition
└── data
    ├─── probe
        ├───PROBE
            ├── seal_1
            │   ├── photo1.png
            │   └── photo2.png
            ├── seal_2
            │   ├── photo1.jpg
            │   └── photo2.jpg
            └── seal_3
                ├── photo1.png
                ├── photo2.png
                └── photo3.jpg
    ├─── unprocessed 
        ├───FOLDERNAME
            ├── seal_1
            │   ├── photo1.png
            │   └── photo2.png
            ├── seal_2
            │   ├── photo1.jpg
            │   └── photo2.jpg
            └── seal_3
                ├── photo1.png
                ├── photo2.png
                └── photo3.jpg
    ├─── processed 
```
In the ./data folder, there should be a probe folder for probe images, unprocessed folder for your unprocessed training data, processed folder where training data will be stored after being pre-processed. 
We will show you how to upload your data to AWS in step 3 of setting up SEALNET

# Connect to AWS for new user

If this is your first time connecting to AWS, you can follow the instructions
below to set up your workspace. 

The instructions assume you are running MacOs or some other Unix-like
system. If you have
Windows installed, you may need to download and install OpenSSH
https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse.
1. Download the ssh key kingram_id_rsa to your Downloads folder.
For instance, if your name is Ahmet Ay, it will be aay_id_rsa.txt.
2. If you are not on the Colgate network, make sure you are connected
to the VPN
3. Start the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking start.
4. Open terminal application from the applications folder
5. Run `cd ~/Downloads/` to change the directory
6. Run `ssh -i kingram_id_rsa.txt kingram@gpu-1.colgate.edu`

NOTE: If you try to log in to AWS and you encounter an error that says:
    WARNING: UNPROTECTED PRIVATE KEY FILE!
Run this command `chmod 400 kingram_id_rsa.txt` in the Downloads folder to
change permissions on your key.

At this step, you are now connected to the AWS cluster. 
Note: To end the AWS session type in 'sudo poweroff' and hit enter
or visit http://hpc-aws-launcher.colgate.edu/ and clicking stop.

The upcoming instructions assume the EC2 instance has been configured by
Colgate ITS. You will need git and latest python3 installed. 
7. Run `cd /data` to access the data directory
8. Run `mkdir kingram_workspace` to create your workspace. This will be
the primary working directory.
9. Run `cd kingram_workspace`
Now you have created your own workspace on the AWS cluster. Whenever you
connect to AWS next time, please cd to this workspace to run your code.

# Setting up SEALNET for new user

The following instructions assume that you are currently in your workspace
on the AWS instance. If you have set up SEALNET before, you can skip this 
step.

1. Run `git clone https://github.com/zbirenbaum/SealFaceRecognition.git` to
download SealNet and run `cd ./SealFaceRecognition`
2.  a. Run `mkdir data && cd data`
    b. Run `mkdir unprocessed && mkdir processed && mkdir probe`
    c. Run `cd ..` 
    This step will create the data/unprocessed folder where you will store your 
    unprocessed photos
3. Make sure that your training data is in the Download folder and is named 'Final_Training_Data'. You should also make sure that no files/folders within Final_Training_Data has a space in their names. 
In a SEPARATE terminal window, run `cd ~/Downloads/` to change
directory. Run 
`scp -i kingram_id_rsa.txt -r PHOTOFOLDER/ kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/data/unprocessed` 
to copy the photos to AWS
4. In the other terminal window still logged into AWS, run `cd SealFaceRecognition` to change directory
5. Create a virtual environment by running:
`python3 -m venv py37`
The AWS instance has python 3.7 as the global python3 version.
6. Activate your virtual environment by running `source ./py37/bin/activate`
7. Install all dependencies by running `pip install -r requirements.txt`. If it gives an error,
run `./py37/bin/python3 -m pip install --upgrade pip` to update pip and run the previous command again.
When you are done with the virtual environment, run `deactivate`

# Accessing SEALNET for returning user

1. Start the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking start.
2. Open a new terminal and connect to AWS by running `cd ~/Downloads/` 
and  `ssh -i kingram_id_rsa.txt kingram@gpu-1.colgate.edu` and click yes if prompted.
NOTE: If you try to log in to AWS and you encounter an error that says:
    WARNING: UNPROTECTED PRIVATE KEY FILE!
Run this command `chmod 400 kingram_id_rsa.txt` in the Downloads folder to
change permissions on your key.
3. Go to your SealNet workspace by running
`cd /data/kingram_workspace/SealFaceRecognition` 
4. Checking for the latest version of the software by running `git pull` 
5. If you need to upload new data, check step 3 of Setting up SEALNET for new user. 
6. Activate your virtual environment by running `source ./py37/bin/activate`.

# Training SEALNET

To train SealNet, make sure you are in the SealNet workspace and is 
currently in the py39 virtual environment.

1. Run `source ../cuda.sh`          
2. Run `sh ./train.sh` to start training
the network with the pre-processed data. Do not close the
terminal window or log out while the program is running.
Alternatively, you can also run `sh ./train.sh 5`
to run a 5 fold cross-validation on the data in FOLDERNAME.

# Using SEALNET for prediction

1. If you have uploaded the probe photos, you can ignore this step.
Otherwise, make sure the probe photos are in the Download folder and run: 
```
cd ~/Downloads
scp -i kingram_id_rsa.txt -r YOUR_PROBE_FOLDER kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/data/probe
```
2. On the terminal connected to AWS, run `sh ./generatePrediction.sh YOUR_PROBE_FOLDER` to run the recognition model on your probe data. It will output a result.json file that you will use to open the GUI.
3. Back on the other terminal, run 
```
cd ~/Downloads
scp -i kingram_id_rsa.txt kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/result.json ./
```
to download the result files into Download folders.

# Close the program

1. When you are done with the program, close the virtual environment by running `deactivate`.
2. Stop the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking stop.

# Additional info:
1. The result.json file will be used in https://github.com/hieudo-hn/recognitionGUI.git.
2. How to open a separate terminal: Right Click on the Terminal Icon and choose New Window.
3. Tips on terminal: Use Tab to autocomplete pathing in your terminal and arrow up to view your previous command 