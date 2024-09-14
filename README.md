# CS50P Project: The runner
#### Video Demo:  <https://youtu.be/s7zOFlsuTP0>
####This is my CS50P final project and here is its description!
#### Description: The game is called "The runner" and is a simple game where the main character has to run and avoid obstacles all while trying to gain the highest score. This project uses python as the language and pygame as the main external module apart from using sys, pytest and random modules too. The overall structure of the project folder is as follows:
>- project.py
>- test_project.py
>- requirements.txt
>- README.md
>- scores.txt
>- bg.jpg
>- Fly
>   - Fly1.png
>   - Fly2.png
>- font
>   - Pixeltype.ttf
>- Player
>   - R1.png
>   - R2.png
>   - R3.png
>   - R4.png
>   - R5.png
>   - R6.png
>   - R7.png
>   - R8.png
>   - R9.png
>- snail
>   - snail1.png
>   - snail2.png
#### in the project.py file we have the follwing functions and classes:
>- functions:
>   - main
>   - collision
>   - score
>- classes:
>   - Player class which has the follwing methods:
>       - __init__
>       - p_ani
>       - gravity
>       - update
>   - Enemies class which has the follwing methods:
>       - __init__
>       - e_ani
>       - destroy
>       - update
#### explaining the project.py file in detail:
#### first we import the necessary modules: pygame, exit from sys, random. After initialising all the files and functions within the pygame module we define two classes, Player and Enemies. Here we take the help of sprites to make the process easier in pygame, these two classes act as the sprites, for this they inherit from the pygame.sprite.Sprite class. Inside the Player class we have __init__ method where we initialise the parent class's attributes as well as initialise our own attributes. All the images of the player are loaded and we define a list of all the images of the player among other things. g or acceleration due to gravity is also defined here. The p_ani method animates the player running(here the player is in the same position but the frames change to show the character running), this is done by cycling through the images in the p_frames list by an index increment of 0.3 every 1 out of 60 frames(where 1s elapsed corresponds to 60 frames shown), the index becomes int(p_index) to ensure that p_index only has integer values, now if the index becomes greater than or equal to the len of the p_frames list, the index is pushed back to 0. gravity method introduces gravity to the game by adding a downward acceleration, rect.y or the y component of the rect of the player increments by g every frame and g gets incremented by 1 every frame, but if rect.y == 350 which indicates the ground then rect.y is kept fixed at 350 to keep it standing on the ground. update method calls the other two methods described above and this method is needed for the class itself to function as a sprite. The Enemy class also is a sprite class which inherits from pygame.sprite.Sprite and takes an argument for the attribute "choice" from the user. We can put in "snail" or "fly" for choice of enemy and this is done randomly with a slight bias as we will see later on. The __init__ method here is defined in much the same way as for the Player class but there is no action of gravity for the enemies. e_ani method is defined in almost the same way as p_ani method but with two cases, one for snail and one for fly. destroy method helps to kill the enemy sprites when they go out of frame to help declutter the game and its screen, and update method calls the above two above mentioned methods, again the update method is required for the class to function as a sprite
#### After that we define a clock variable and define variables for the bg image, the various texts that make up the buttons. Then we define and add the Player class to a GroupSingle variable whose name is player which is a Group container which holds a single sprite in this case that of the player, we also define a Group of name enemies which hold a group(here group of 2) of sprites, which in this case are flies and snails.
#### Next we define two functions, collision and score. The collision function checks for collision between two sprites, so we use pygame.sprite.spritecollide(sprite, Group, True/False) to do that, this method checks for collision between a single sprite and a Group of sprites(flies, snails) and returns a list with all the sprites that interact with a Group. So in the collision function we return False if that list is filled with atleast one element and True if its filled with no elements, and this return value will later on in the main loop be associated with the game_start variable which tells if the main game screen is running or no. So if collision() returns False, that is collision occured then the main game screen no longer runs. The score function return the score and works based on timers. Per second survived gives the player 10 points. score variable is defined as the (time elapsed from the click of the start button)/100 minus the (filler time)/100. Since timers cannot be stopped once they start or are called they continue recording time and hence they end up recording the time spent in the restart window as well which is not to be counted when finding the score in the main game screen, hence we subtract the filler time which is a timer which starts its count the moment we go to the restart screen and continues from there. This ensure that the score is always set to 0 at the beginning of the game each time. In this function we also blit the score itself and other related text on the screen. After defining these two functions we define a custom event which is called every 1 second, and based on this event we will spawn our enemies.
#### now we move to the main function which holds the main event loop of the game. First we define a few variables which will be needed later on, like hs or highestScore which holds the highest score of current iteration of the game played, start_screen which is True if start screen is displayed, game_start which is True if the main game screen is displayed and restart which is True if the restart screen is displayed. The while loop is defined to run 60 times a second as is shown at the end of the while block with clock.tick(60), this determines the frame rate which in this case is 60 fps. In the while loop we first define all the events that could happen and what to do if they occur. The first event deals with clicking on the cross button on the top right corner, if that is done then sys.exit() is called which closes the game, and the other lines of code written for this event block is to set the highest score to 0 in the scores.txt file so that a fresh start can be achieved once the game runs from the start again. The next event is if the start button which appears on the start screen is clicked which then sets game_start to True to take the game to the main game screen and sets the start_screen and restart variables to False. The next event is if game_start is True and the custom event we created is triggered then we add the class Enemies to the enemies Group with random.choice(['snail', 'snail', 'snail', 'fly']) as an argument to the choice attribute. random.choice helps to pick a value from 'snail' or 'choice' with 75 percent chance of picking snail and 25 percent change of picking fly and hence the bias for snail. This means that on avg we will see more snails in the game than flies. The next event is if game_start is False which then lets restart variable be True taking the gane to the restart screen. Also, here we open and read the scores.txt file and add the highest score given there to the set hs_set(assuming that score is already not present otherwise it will not be added since sets cannot have duplicate values). The next event is if we click on the restart button in the restart screen which then takes us back the main game screen and also clears all the enemy sprites by using enemies.empty() to start the game fresh. After than we blit the bg to the screen and define some if-elif and if block of code corresponding to the states of the game(start, main game, restart), the first one for start screen where we just blit the "start" text onto the screen, then for the second block of code for main game screen, we blit the text for "score", "highest score", draw and update the enemies, in this block we also call the collision and score functions that we defined before, and we also blit the scores and highest scores numbers. We also in this block of code pick the highest number among the set of highest scores in hs_list by using a for loop and assign it to hs variable. We then display this variable for the highest current score. The hs stores the  highet score of the current iteration of the game. In the next elif block, we move to the restart screen where we dont update the player or enemies using the .update() method to ensure that the last frame before the main game screen ended is shown in the restart screen to show where the player went wrong. Here we also open the scores.txt file to check if the current score is higher than the previous highest score as is mentioned in the scores.txt file in which case that value will be updated in the text file now. The scores.txt text file contains only a single line with the current highest score mentioned in it always. Then we close the file opened. The next independent if block says that only if the game is in the start screen or the main game screen the player should update its values, that is "move" else in case of the restart screen it will not update its values and be still. At the end we finally call main() and the whole code starts running.
#### in test_project.py we have the follwing functions:
>- test_coll1
>- test_coll2
>- test_coll3
>- test_score1
>- test_score2
>- test_player1
>- test_player2
>- test_enemy1
>- test_enemy2
#### in the test_project.py file we test for the functions and methods mentioned in the project.py file. First we import all the functions and classes from project.py and import pytest to test for errors. test_coll1 tests if the return value for the collision function gives only True or False. test_coll2 tests if return value for collision function is not 'true' or 'false' in strings. test_coll3 tests if the return type for collision function is bool. test_score1 tests if return type of the score(12342) function is int. test_score2 tests if Type error is raised if score('hello') is called, in this case with keyword is used. test_player1 tests if the p_index attribute of the Player class is set to 0 based on the conditions of p_ani method. test_player2 tests if y component of rect attr and g attr are set to 350 and 0 respectively based on the conditions of gravity method. test_enemy1 tests if index attribute of Enemies("snail") is incremented by 0.3 per frame. test_enemy2 tests if TypeError is raised when instance of Enemies() is called since no arg for choice attr is given. 
#### in requirements, the modules required are mentioned, in this case they are pygame, pytest.
#### in scores the current highest score of the game is stored.
#### Fly, font, snail, Player are all assets of the game. The Fly folder has images of the fly enemy as pngs, the snail folder has images of the snail enemy, the Player folder has images of the player/runner itself, and font folder has a font type stored in a ttf(TrueType font) format and bg.jpg contains the background picture of the game
#### README.md is this file where the description of the project, its name and a video of the project is kept.
