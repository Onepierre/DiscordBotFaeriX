# Discord Bot for FaeriX chads
To add it to your server, create your own bot on discord dev panel and use the code in main.py.
It runs with Python3.7. 

## Use Astrid's advices.
Use the command 
```?astrid```
to create and send a picture showing a proverb taken in the file ```astrid/quotes_win.txt```. If you are Linux user, you can use accents while adding them to the file. 

## Display XKCD comics
Use the command 
```?xkcd [arg]```.  
It will send in the channel a xkcd comic depending on the value of arg.  
If arg is a positive number, it will sent the corresponding xkcd comic.  
If arg is a negative number, it will sent the corresponding xkcd comic counting from the last published one.  
If arg is ```"last"```, it will sent the last xkcd comic.  
If arg is not given, it will sent a random xkcd comic. 

## Display Cardboard Crack comics
Use the command 
```?mtg [arg]```.  
It will send in the channel a Cardboard Crack comic depending on the value of arg.  
If arg is a positive number, it will sent the corresponding Cardboard Crack comic.  
If arg is a negative number, it will sent the corresponding Cardboard Crack comic counting from the last published one. 
The cartoons must be in a folder named cardboard_crack as no API is existing.

## Stop bot
The command
```?exit``` stops the bot.