# Online-Board-Game
Creating Online Board Game Using Socket and Tkinter 


## Game Description 

in this simple 2-player board game, each player must press the dice button and wait for the other player to press the dice button. each time a number will appear randomly on the GUI and the player moves accordingly.

players can chat with each other using the chatbox. 

there are some numbered and "?" locations on the board. each time a player moves into one of these "?" locations, a stranger sends a message to that player. this message only can be seen by the player who is inside the "?' location ( it won't be sent to the other player).
the stranger gives you some clues about the crime(such as the killer's hair color, age and etc.). 

### the stranger messages can be categorized as below:
~~~
1. useful and correct information about the killer
2. wrong information to mislead you 
3. useless information
~~~

whenever one of the players reaches the location with the number 60, a pop-up window will be displayed with 10 suspects. there is some information about each suspect and you must select the killer according to the information you've got from the stranger.

### players have the options below:
~~~
1. cooperate with each other and share the information they get from the stranger
2. try to mislead each other by giving wrong information
3. do not use the chatbox and trust the stranger (and their chance)
~~~

### More Information
	

1. your location will be displayed by blue ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) color and 
the opponent location will be displayed by red 
![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)  color
2. if both players are in the same location it will be displayed by green ![#008000](https://via.placeholder.com/15/008000/000000?text=+) color
3. whenever a player reaches a "?" location, it will be displayed with gray ![#808080](https://via.placeholder.com/15/808080/000000?text=+) color for the other player


## How to run

~~~
1. install requirments.txt using the command below
    1.1 pip install -r requirements.txt
2. run Server.py file
3. run Gui.py
    3.1 enter your nickname 
    3.2 wait for other player to join
4. run Gui.py again from another CLI
    4.1 enter your nickname
    4.2 press on dice button

~~~

### First Player
![1](https://user-images.githubusercontent.com/47816410/137785171-c1938ca4-0936-4333-9998-be0b6adbe848.jpg)

![1 1](https://user-images.githubusercontent.com/47816410/137785265-db225fda-e782-4422-a4a6-04d6c075f0b9.jpg)

### Second Player

![2](https://user-images.githubusercontent.com/47816410/137785395-93f9cf84-2c27-4fd7-9189-6d29a99c8d4e.jpg)

![2 1](https://user-images.githubusercontent.com/47816410/137785460-f6ab5c41-9cd6-44e4-aef7-673d7fe54329.jpg)



### The GUI

![3](https://user-images.githubusercontent.com/47816410/137790171-905da3ec-69c1-4cdc-850e-60c52f2dd1ff.jpg)


### Suspects popup

images have been generated using AI 

![4](https://user-images.githubusercontent.com/47816410/137790548-1be677e0-15dc-4c3e-bba4-567b764145ba.jpg)
