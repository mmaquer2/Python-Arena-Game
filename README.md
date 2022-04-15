# 2d Zelda-like arena game with randomly assinged NPC AI personalities and behavior 


[Image]

## Description: 
- This served as a final Project for CS5150 (Game AI) at Northeastern University, Spring 2022. The project is a 2d arena fighting game with action rpg mechanics. The game contains 3 NPC characters and one human player. Each is randomly assigned a weapon and stats, and is placed in the map all to fight each other until a single victor emerges.

- **Note** This program will only work on a windows system due to file path constraints, I have not yet transferred the code to a common file path system

## CPU AI Behavior: 

- Randomly Selected Personalities: 
    - The behavior and strategy of the AI is selected at random from a collection of different prebuilt strategies and actions. 

- Possible AI Strategies and Personalities:
    - bersek mode, enemy will find the nearest target lock and and might until destoryed and victory is reached 
    - ambush, wait for enemies to enter a specific radius of the CPU and attack
    - patrol area, wander around a set path with waypoints, and attack units when they are found
    - flee and hide, avoid being attacked at all costs, will use block a lot.

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

## Player Controls

- movement, arrow keys
- primary attack, space bar
- block/defend, b letter key


## Resources and Credits
- https://www.pygame.org/docs/
- https://pypi.org/project/pathfinding/
- Special Thanks to the clear code youtube channel, for providing starter code and boilerplate for the game main loop 
- Pixel ninja on itch.io ( https://pixel-boy.itch.io/ninja-adventure-asset-pack ) for providing free art assets used for the game's characters and environment 
- Procedural Content Generation using Behavior Trees (PCGBT) by 
Anurag Sarkar and Seth Cooper



## License 

This project is published under the Creative Commons Zero (CC0) license.
