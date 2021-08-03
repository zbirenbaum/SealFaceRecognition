--------------------------------
SEALNET USER GUIDE
--------------------------------
This document is intended as a detailed guide to help with
installation and running of
SealNet, a face recognition software for Harbor Seals. The
instructions are intended to
run the software on Amazon Web Services (AWS) EC2 cluster running
Linux but they can be
modified for use on other setups running Linux or other Unix-like
systems.
To run a command, type it out on the terminal and hit enter.
--------------------------------
DATA
--------------------------------
SealNet is a face recognition software that is trained using photos.
As of now, the software
expects files of png, jpg and jpeg formats.
The directories must be structured as follows:
.
├── SealFaceRecognition
└── data
    ├─── unprocessed 
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
The photos directory will then be copied to AWS as shown in step 2 of
'SET UP SEALNET'
--------------------------------
CONNECT TO AWS FOR NEW USER
--------------------------------
The instructions assume you are running MacOs or some other Unix-like
system. If you have
Windows installed, you may need to download and install OpenSSH
https://docs.microsoft.com/en-us/windows-server/administration/
openssh/openssh_install_firstuse.
1. Download the ssh key YOURNAME_id_rsa to your Downloads folder.
For instance, if your name is Ahmet Ay, it will be aay_id_rsa.
2. If you are not on the Colgate network, make sure you are connected
to the VPN
3. Start the aws instance by visiting http://hpc-aws-
launcher.colgate.edu/ and clicking start.
4. Open terminal application from the applications folder
5. Run 'cd ~/Downloads/' to change the directory
6. Run 'ssh -i YOURNAME_id_rsa YOURNAME@gpu-1.colgate.edu'
At this step, you are now connected to the AWS cluster. 
Note: To end the AWS session type in 'sudo poweroff' and hit enter
or visit http://hpc-aws-launcher.colgate.edu/ and clicking stop.
--------------------------------
INSTALL THE VIRTUAL ENVIRONMENT
--------------------------------
These instructions assume the EC2 instance has been configured by
Colgate ITS. You will need
git and latest python3 installed. After logging in to AWS,
1. Run 'cd /data' to access the data directory
2. Run 'mkdir YOURNAME_workspace' to create your workspace. This will be
the primary working directory.
3. Run 'cd YOURNAME_workspace'
4. Run 'wget https://repo.anaconda.com/archive/Anaconda3-2020.02-
Linux-x86_64.sh' to download the
   Anaconda installer.
5.  a. Run 'bash Anaconda3-2020.02-Linux-x86_64.sh' to start the
installation process.
    b. Hit enter for the first prompt
    c. Hit q to skip to the end of the license, type yes for the
prompt and hit enter.
    d. Type in '/data/YOURNAME_workspace/anaconda3' for the install
location and hit enter
    e. Type yes for the next prompt and hit enter
    The installation is now complete
6.  a. Run 'exit' to log out of AWS.
    b. Run 'ssh -i YOURNAME_id_rsa YOURNAME@gpu-1.colgate.edu' to log in again
7.  a. Run 'conda create --name myenv python=3.7' to create a
conda environment.
    b. Type y and hit enter at the prompt.
--------------------------------
SET UP SEALNET
--------------------------------
1. Run `git clone https://github.com/zbirenbaum/SealFaceRecognition.git` to
download SealNet
2.  a. Run `mkdir data`
    b. Run `cd data`
    c. Run `mkdir unprocessed` 
    This step will create the data/unprocessed folder where you will store your 
    unprocessed photos
3. a. Download the unprocessed photos for training SealNet to your Downloads
folder in a folder named photos
    b. In another terminal window, run 'cd ~/Downloads/' to change
directory
    c. Run 'scp -i YOURNAME_id_rsa -r PHOTOFOLDER/ YOURNAME@gpu-1.colgate.edu:/data/
YOURNAME_workspace/SealFaceRecognition/data/unprocessed' to
       copy the photos to AWS
4. In the other terminal window still logged into AWS, run 'cd
SealFaceRecognition' to change directory
5. Install dependencies found in requirements.txt by running the
commands below. For each command
   run the command and then type in y at the prompt and hit enter.
    a. 'conda activate myenv'
    b. 'conda install --file requirements.txt'
--------------------------------
RUNNING
--------------------------------
These instructions assume that the project has been set up as in
previous instructions.
Revisit 'CONNECT TO AWS' instructions above to connect to AWS from
terminal application.
The rest of these steps assume you are connected to AWS. Type the
commands in the terminal window
without the quotes and then hit enter to run them.
If you need to run SealNet using new data, make sure it is formatted
properly as shown in 'DATA'
above. Open a new terminal window and then use step 2 in 'SET UP
SEALNET' to copy the data to AWS.
Once the data is ready, go back to the previous terminal window still
logged in to AWS.
1. Run 'cd /data/aylab_workspace/SealFaceRecognition' to change
directory
2. Run 'git pull' to get the latest changes from GitHub
3. Run 'conda activate aylab_env' to start the virtual environment
4. Run 'python train.py -c config.py -d ../photos' to start training
the network. Do not close the
   terminal window or log out while the program is running.
5. Run 'sudo poweroff' to end the AWS session or visit http://hpc-aws-
launcher.colgate.edu/ and
   click stop
--------------------------------
RESULTS
--------------------------------
The results are located in log/result.txt. The log directory is a list
of all results and
checkpoints by the software with each folder containing one run of the
program.
To copy the results to your local machine:
 
1. Open a terminal window on your machine (not logged in to AWS) from
applications folder
2. Make sure you are connected to the VPN and start AWS at http://hpc-
aws-launcher.colgate.edu/.
3. Run 'cd ~/Downloads' in the terminal to change directories
4. Run 'scp -i aay_id_rsa aay@gpu-1.colgate.edu:/data/aylab_workspace/
SealFaceRecognition/log/result* ~/Downloads/' to copy all the results
files.
NOTE:
If you try to log in to AWS and you encounter an error that says:
    WARNING: UNPROTECTED PRIVATE KEY FILE!
Run this command 'chmod 400 aay_id_rsa' in the Downloads folder to
change permissions on your key.
To reproduce results from the paper:
1. Log in to AWS.
2. Run 'cd /data/aylab_workspace/SealFaceRecognition' to change
directory
3. Run 'git pull' to get the latest changes from GitHub
4. Run 'conda activate aylab_env' to activate the virtual environment.
5. Run 'bash run_training.sh'