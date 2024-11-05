import logging
import os
import sys
from datetime import datetime

# Why?
# Answer: Debugging the excption handling, Error Management, We make logs to have checks of the working of the projects.


####### DELETE THE FOLDER "logs" from LiveSensor_FULL_MLProject(parent) #######

# We will give file name as creation time of that file..
# So that we have a idea of the file..
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # .now current time.. will eb in numeric # convert it into string

#Make the folder to store the file
logs_path= os.path.join(os.getcwd() ,"LiveSensor_FULL_MLProject/logs", LOG_FILE) # make the path to join the file and the folder 
# FIRST ENTRY (in the join() function) - to capture the current dictory to locate the file for errors 
# SECOND ENTRY (in the join() function) - name the folder - given by US
# THIRD ENTRY (in the join() function) - attach the log file with the folder

os.makedirs(logs_path,exist_ok=True) # Flag True when logs_path is already formed

LOG_FILE_with_PATH=os.path.join(logs_path,LOG_FILE)



logging.basicConfig(
    filename=LOG_FILE_with_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", 
    # The s stands for "string" and indicates that the timestamp should be formatted as a string. 
    # The d stands for "decimal" and indicates that the line number should be formatted as an integer.
    level=logging.INFO 
)

    # Five Levels:
    #     1. debug
    #     2. info
    #     3. Warning
    #     4. errors
    #     5. critical

# Example log messages
logging.info("Logging setup complete.")