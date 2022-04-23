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

The instruction here is an example of how to access the terminal for user named Krista Ingram.
If you have your own account, please replace kingram with your account name (for instance, Ahmet Ay should be aay).

## Prerequisite

To run this program we need python 3.7 installed. You can check your python version
by typing `python3 -V`. If you don't have python 3.7, you can download it here:
https://www.python.org/downloads/release/python-379/.

If you are using the AWS cluster, it is already installed for you.

You will also need to have Visual Studio Code installed. If you do not have VS Code, you can download it from here:
https://code.visualstudio.com/download

## Data

SealNet is a face recognition software that is trained using photos.
As of now, the software expects files of png, jpg and jpeg formats.
The directories must be structured as follows:
```
.
├── SealFaceRecognition
    ├───data
        ├──processed
            |-- train
            |-- probe
        ├──unprocessed 
            |-- train
               ├──Final_Training_Dataset
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
            |-- probe
                ├──Your_Probe_Set


```
In the ./data folder, there should be a processed and an unprocessed folder. All initial data should be placed in the unprocessed folder. From the SealFaceRecognition root directory run `python zprocess.py` which will create processed counterparts in 'data/processed' for each of the datasets contained in unprocessed. We have included our dataset as an example under 'final_dataset'. To run the model on this example, simply move final_dataset/Final_Data to data/unprocessed/
We will show you how to upload your data to AWS in step 3 of setting up SEALNET

## Connect to AWS for new user

If this is your first time connecting to AWS, you can follow the instructions
below to set up your workspace. 

The instructions assume you are running MacOs or some other Unix-like
system. If you have
Windows installed, you may need to download and install OpenSSH
https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse.
1. Download the ssh key kingram_id_rsa to your Downloads folder.
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

## Setting up SEALNET for new user

The following instructions assume that you are currently in your workspace
on the AWS instance. If you have set up SEALNET before, you can skip this 
step.

1. Run `git clone https://github.com/zbirenbaum/SealFaceRecognition.git` to
download SealNet and run `cd ./SealFaceRecognition`
2. Setting up the data folder: 
```
mkdir data && mkdir data/processed && mkdir data/unprocessed && mkdir data/unprocessed/train && mkdir data/unprocessed/probe && mkdir data/processed/train && mkdir data/processed/probe
```
3. Make sure that your training data is in the Download folder and is named 'Final_Training_Dataset'. You should also make sure that no files/folders within Final_Training_Dataset has a space in their names. 
In a SEPARATE terminal window, run `cd ~/Downloads/` to change
directory. Run 
```
scp -i kingram_id_rsa.txt -r Final_Training_Dataset kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/data/unprocessed/train
```
to copy the photos to AWS.
Similarly, if you have new probe folders, make sure that it is named probe_folder_test and is located in the Downloads folder on your local laptop. Then run:
```
scp -i kingram_id_rsa.txt -r probe_folder_test kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/data/unprocessed/probe
```

4. In the other terminal window still logged into AWS, run `cd SealFaceRecognition` to change directory
5. Create a virtual environment by running:
`python3 -m venv py37`
The AWS instance has python 3.7 as the global python3 version.
6. Activate your virtual environment by running `source ./py37/bin/activate`
7. Install all dependencies by running `pip install -r requirements.txt`. If it gives an error,
run `./py37/bin/python3 -m pip install --upgrade pip` to update pip and run the previous command again.
When you are done with the virtual environment, run `deactivate`

## Setting up VS Code 
1. Open Terminal in VS Code by clicking the Terminal button.
2. Copy your rsa_file into .ssh folder:
```
cp ~/Downloads/kingram_id_rsa.txt ~/.ssh/
```
3. Install remote-ssh extension on VS Code: you can do so by clicking on the 4-square icon on the left sidebar and search for Remote - SSH. Then click install.
4. Then Open the VS Code's command palette by doing Command-Shift-P and search for Remote - SSH: Open SSH Configuration File and paste the following into the config file:
```
Host gpu-1.colgate.edu
    HostName gpu-1.colgate.edu
    User kingram
    IdentityFile ~/.ssh/kingram_id_rsa.txt
    IdentitiesOnly yes
```

## Accessing SEALNET for returning user

1. Start the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking start.
2. Open VS Code, then open the Terminal on VS Code by clicking Terminal. Connect to the AWS server by clicking the icon >< in the bottom right of VS Code, then choose "Connect to Host", and click on "gpu-1.colgte.edu"
3. Navigate to your SealNet workspace in the folder /data/kingram_workspace/SealFaceRecognition.
4. On the terminal, checking for the latest version of the software by running `git pull` 
5. **[ONLY DO THIS STEP IF YOU ARE TRAINING WITH NEW DATA]** Run `sh ./clean.sh`, this will delete all training and probe folders on the AWS cluster. Then you can drag your training folder from your local laptop into the data/unprocessed/train folder on the AWS cluster. Likewise, drag your probe folder from your local laptop into the data/unprocessed/probe folder on the AWS cluster.
6. Activate your virtual environment by running `source ./py37/bin/activate`.
7. Run `source ../cuda.sh`  

## Training SEALNET

To train SealNet, make sure you are in the SealNet workspace and is 
currently in the py39 virtual environment.
        
1. Run `sh ./train.sh` to start training
the network with the pre-processed data. Do not close the
terminal window or log out while the program is running.
Alternatively, you can also run `sh ./train.sh 5`
to run a 5 fold cross-validation on your data.

## Using SEALNET for prediction
1. If you have uploaded the probe photos, you can ignore this step. Otherwise, drag your probe folder from your local laptop into the data/unprocessed/probe folder on the AWS cluster.
2. On the terminal connected to AWS, run `sh ./generatePrediction.sh` to run the recognition model on your probe data. It will output a result.json file that you will use to open the GUI.
3. Back on the Desktop terminal, run 
```
cd ~/Downloads
scp -i kingram_id_rsa.txt kingram@gpu-1.colgate.edu:/data/kingram_workspace/SealFaceRecognition/result.json ./
```
to download the result files into Download folders.

## Close the program

1. When you are done with the program, close the virtual environment by running `deactivate`.
2. Stop the aws instance by visiting http://hpc-aws-launcher.colgate.edu/ and clicking stop.

## Additional info:
1. The result.json file will be used in https://github.com/hieudo-hn/recognitionGUI.git.
2. How to open a separate terminal: Right Click on the Terminal Icon and choose New Window.
3. Tips on terminal: Use Tab to autocomplete pathing in your terminal and arrow up to view your previous command 
