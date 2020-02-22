# What is screntime-reporter?
screentime-reporter (STR) was developed over my mid-winter break as my first 'real' project. The purpose of this project was not to check how much time was spent on the computer, as we all know we spend too much time on the computer, but how we are spending that time. This is supposed to then help with productivity and other things

## What does screentime-reporter do?  
STR checks for the active application at intervals determined by the user. At the end of the week, the script will then send the week's and all time statistics to user's email. 

## What are libraries needed for this tool? 
As of now:   
1. matplotlib (for graphing)   
2. psutil (for monitoring)

## What are the known issues?
1. The way the name of the active application is found prevents the application from finding the real name but rather the file name. This will be improved on in the future. 

## Future Ideas
1. Change log format from:   
(Name) : (Time) => csv file   
2. Better HTML email design
3. Block applications that you deem as a waste of time
4. Tracking websites
5. Blocking websites
