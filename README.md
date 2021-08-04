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
We will show you how to upload your data to AWS in step 3 of setting up SEALNET

# Connect to AWS for new user

If this is your first time connecting to AWS, you can follow the instructions
below to set up your workspace. 

The instructions assume you are running MacOs or some other Unix-like
system. If you have
Windows installed, you may need to download and install OpenSSH
https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse.
1. Download the ssh key YOURNAME_id_rsa to your Downloads folder.
For instance, if your name is Ahmet Ay, it will be aay_id_rsa.txt.
2. If you are not on the Colgate network, make sure you are connected
to the VPN
3. Start the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking start.
4. Open terminal application from the applications folder
5. Run `cd ~/Downloads/` to change the directory
6. Run `ssh -i YOURNAME_id_rsa.txt YOURNAME@gpu-1.colgate.edu`

NOTE: If you try to log in to AWS and you encounter an error that says:
    WARNING: UNPROTECTED PRIVATE KEY FILE!
Run this command 'chmod 400 YOURNAME_id_rsa.txt' in the Downloads folder to
change permissions on your key.

At this step, you are now connected to the AWS cluster. 
Note: To end the AWS session type in 'sudo poweroff' and hit enter
or visit http://hpc-aws-launcher.colgate.edu/ and clicking stop.

The upcoming instructions assume the EC2 instance has been configured by
Colgate ITS. You will need git and latest python3 installed. 
7. Run `cd /data` to access the data directory
8. Run `mkdir YOURNAME_workspace` to create your workspace. This will be
the primary working directory.
9. Run `cd YOURNAME_workspace`
Now you have created your own workspace on the AWS cluster. Whenever you
connect to AWS next time, please cd to this workspace to run your code.

# Setting up SEALNET for new user

The following instructions assume that you are currently in your workspace
on the AWS instance. If you have set up SEALNET before, you can skip this 
step.

1. Run `git clone https://github.com/zbirenbaum/SealFaceRecognition.git` to
download SealNet
2.  a. Run `mkdir data && cd data`
    b. Run `mkdir unprocessed && mkdir processed`
    c. Run `` 
    This step will create the data/unprocessed folder where you will store your 
    unprocessed photos
3. a. Download the unprocessed photos for training SealNet to your Downloads
folder in a folder named photos
    b. In a SEPARATE terminal window, run 'cd ~/Downloads/' to change
directory
    c. Run 
`scp -i YOURNAME_id_rsa.txt -r PHOTOFOLDER/ YOURNAME@gpu-1.colgate.edu:/data/YOURNAME_workspace/SealFaceRecognition/data/unprocessed` 
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
2. Connect to AWS by running `cd ~/Downloads/` 
and  `ssh -i YOURNAME_id_rsa.txt YOURNAME@gpu-1.colgate.edu`
3. Go to your SealNet workspace by running
`cd /data/YOURNAME_workspace/SealFaceRecognition` 
4. Checking for the latest version of the software by running `git pull` 
5. Activate your virtual environment by running `source ./py37/bin/activate`.
When you are done with the virtual environment, run `deactivate`.
6. Stop the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking stop.

# Training SEALNET

To train SealNet, make sure you are in the SealNet workspace and is 
currently in the py39 virtual environment.

1. Run `python zprocess.py FOLDERNAME` to pre-process all photos in 
/data/unprocessed/FOLDERNAME 
2. Run `python train.py -c config.py -d ./data/processed/FOLDERNAME` to start training
the network with the pre-processed data. Do not close the
terminal window or log out while the program is running.
Alternatively, you can also run `python train.py -c config.py -d ./data/processed/FOLDERNAME -n 5`
to run a 5 fold cross-validation on the data in FOLDERNAME.

# Using SEALNET for prediction

1. Run `python seenbefore.py` to run the recognition model on your probe data. It will output 
a result.json file that you will use to open the GUI.
2. On a SEPARATE terminal, run `cd ~/Downloads` and
`scp -i YOURNAME_id_rsa.txt YOURNAME@gpu-1.colgate.edu:/data/YOURNAME_workspace/SealFaceRecognition/result.json ~/Downloads/`
to download the result files into Download folders.
3. Run 'sudo poweroff' to end the AWS session or visit http://hpc-aws-launcher.colgate.edu/ 
and click stop
