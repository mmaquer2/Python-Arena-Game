# 2d Zelda-like arena game with assinged NPC AI personalities


![project screenshot](https://github.com/mmaquer2/Python-Arena-Game/blob/main/src/sprites/screen_shot.png)

## Description: 
- This served as a final Project for CS5150 (Game AI) at Northeastern University, Spring 2022. The project is a 2d arena fighting game with action rpg mechanics. The game contains 3 NPC characters and one human player. Each is randomly assigned a weapon, and is placed in the map all to fight each other until a single victor emerges.

- **Note** This program will only work on a windows system due to file path constraints, I have not yet transferred the code to a common file path system

## CPU AI Behavior: 
- The CPU AI are given each a different personality to drive their behaviour during the game.
- CPU A, balenced, cpu A will wander around the map and attempt to look for an enemy to attack, and will lock onto a character within its viewable range, then attempt to attack
- CPU B, aggressive, cpu b will immediately lock onto the neartest character then attack until it wins or is defeated.
- CPU C, timid, will hide and attempt to "ambush" players when they walk into a range near the character and attempt to flee when its health level drops below a certain threshold

- Pathfinding:
- Pathfinding was implemented using the python core libraries 

## Setup and Settings
- Download the source directory onto your machine 
- Ensure python 3.0x in installed on your machine 
- To change game window dimensions update the window height and width variable in settings.py
- Navigate to the src directory and run the game.py file or with your cli


## Setup and Usage

```bash

# ensure python 3.0x is installed on your machine
python -v

# install the pygame framework with pip 
pip install pygame

# then verify it was intalled correctly
pygame -v

# With your cli of choice navigate to the src directory and run the following command to start the game

python main.py 

``` 

## Controls
- movement, arrow keys
- primary attack, space bar
- block/defend, b letter key
- p, pause game
- u, unpause game

## Resources and Credits
- https://www.pygame.org/docs/
- https://pypi.org/project/pathfinding/
- Special Thanks to the clear code youtube channel, for providing starter code and boilerplate for the game main loop 
- Pixel ninja on itch.io ( https://pixel-boy.itch.io/ninja-adventure-asset-pack ) for providing free art assets used for the game's characters and environment 
- Procedural Content Generation using Behavior Trees (PCGBT) by 
Anurag Sarkar and Seth Cooper



## License 

This project is published under the Creative Commons Zero (CC0) license.
