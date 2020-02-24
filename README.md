# What is screntime-reporter?
screentime-reporter (STR) was developed over my mid-winter break in my freshman year in high school as my first 'real' project. The purpose of this project was not to check how much time was spent on the computer, as we all know we spend too much time on the computer, but how we are spending that time. This is supposed to then help with productivity and other things

## Installation
1. Run (while in project directory):   
`py main.pyw -s`

2. Install dependencies    

3. Use Windows Task Scheduler to run script on log-on:   
  * Click "Create Basic Task..." on the right.
  * Give the task a name, e.g. "STR" and a description and click "Next >".
  * Click "When I log on" and then "Next >".
  * Then click "Start a program" and "Next >".
  * Then attach pythonw.exe as the program and main.pyw's path as an argument.     
  * Then click "Finish"

## What does screentime-reporter do?  
STR checks for the active application at intervals determined by the user. At the end of the week, the script will then send the week's and all time statistics to user's email. 

## Subscription
To subscribe to weekly email (default):       
(while in project directory)            
`py main.pyw --sub`

To unsubscribe from weekly email:        
(while in project directory)        
`py main.pyw --unsub`

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
