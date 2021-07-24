# Discord Bot for FaeriX chads
To add it to your server, create your own bot on discord dev panel and use the code in main.py.
It runs with Python3.8. 

You need to get a discord connection token and put it in `~/token.txt`
Then use the following command :
```python3.8 main.py```

If you need a launcher on the desktop, use the `launcher.desktop` to do this (for ubuntu). Do not forget to modify the path written on if.

## Function examples

## Help
To get more precise description of functions available, use the command ```?help``` to get a list of functions, or ```?help name``` to get a description of a specific function.


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

