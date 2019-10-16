#######################################################################
#  Copyright [2019] [Riley Eaton]
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
########################################################################
# library imports
import time
import math
import numpy
import random
from tkinter import *
# variable declaration
size = 10  # the number of squares wide & tall the simulation will be (n x n square where size = n)
learningRate = 0.80  # the learning rate, included in the Q-Learning algorithm (between 0 and 1)
discountRate = 0.70  # the discount rate, included in the Q-Learning algorithm (between 0 and 1)
score = 0  # counts how many consecutive times the mouse has reached the cheese
minimumMoves = 0  # to be calculated, the optimum moves from the mouse to the cheese (does not account for obstacles)
cheeseCount = 0  # number of times the cheese has been reached
previousMoves = 0  # the number of moves the mouse previously took to reach the cheese
sameMoves = 0  # counts how many consecutive times the mouse has reached the cheese in the same number of moves
moves = 0  # the number of moves the mouse has taken at any point in time since it has last died
count = 0  # the number of iterations the mouse has gone through
speed = 0  # the user input between 1 and 5 which will dictate the value of refresh (below)
refresh = 0  # the number of milliseconds the program waits to refresh the screen
looping = True  # to control the main while loop
learning = True  # to control the secondary while loop (while the program is learning)
caught = False  # to indicate if the user has entered an invalid input
speed_check = True  # used for the while loop which asks the user for their desired speed
last_run = True  # to indicate if the last iteration is happening, this is so that it can play the path in slow-motion
QTable = [[float(0), float(0), float(0), float(0)]]  # declaration of the Q table
for i in range(0, (size*size*size*size)):  # using a for loop to initialize the Q table with values of 0
    QTable = numpy.append(QTable, [[float(0), float(0), float(0), float(0)]], axis=0)
# entire program loop
while looping:
    # prompt the user for their desired speed of the program and loop until a valid value is given
    while speed_check:
        caught = False  # set caught to false every time the loop loops to ensure correct error message
        print("Enter a number between 1 and 5 to determine the speed of the simulation where 1 is equivalent to real "
              "time & 5 is 20x that")
        try:
            speed = int(input(""))
        except:  # if the user enters anything other than a number, set caught to true and display an error message
            caught = True
            print("You have provided an invalid input. Please enter a number")
        # set the refresh speed according to the users input
        if 1 <= speed <= 5:
            if speed == 1:
                refresh = 100
            elif speed == 2:
                refresh = 75
            elif speed == 3:
                refresh = 50
            elif speed == 4:
                refresh = 25
            elif speed == 5:
                refresh = 5
            speed_check = False  # exit the while loop
        else:  # if the entered value was not between 1 and 5 print an error message accordingly
            if not caught:  # if there was an invalid number, print accordingly
                print("You have given an invalid input. Please enter a number between 1 and 5")
    tk = Tk()  # this is so that i can reference Tk() as tk instead
    tk.title("Machine Learning Mouse")  # give the window a title
    tk.resizable(0, 0)  # make the window unable to be resized
    canvas = Canvas(tk, width=(size * 20), height=(size * 20))  # set the height of the window in proportion to 'size'
    canvas.create_rectangle(-10, -10, (size * 21), (size * 21), fill="black")  # set the background to back
    print("The simulation will automatically terminate once the mouse has conclusively determined the optimal number "
          "of moves to the cheese")
    # create the image variables to be called later
    cheese_image = PhotoImage(file='res/cheese.png')
    bomb_image = PhotoImage(file='res/bomb.png')
    mouse_image = PhotoImage(file='res/mouse.png')
    start = time.time()  # start the timer to be referenced at the end of the program
    # loop while the program is learning (searching for the cheese)
    while learning:
        count = count + 1  # add 1 to the iteration number
        dead = False  # used for a while loop to update various events while the mouse is still moving & not dead
        canvas.pack()  # this and the command below update the entire canvas and allow it to be displayed
        tk.update()
        for x in range(0, size):  # draw the white lines which create the grid
            canvas.create_line((x * 20), 0, (x * 20), (size * 20), fill="white")
            canvas.create_line(0, (x * 20), (size * 20), (x * 20), fill="white")

        # the mouse class
        class Mouse:
            # initializer method to set the first values of the mouse & create the variables needed
            def __init__(self, mouse_canvas):
                self.canvas = mouse_canvas
                self.x_coord = 8  # the x grid unit which the mouse is first located in
                self.y_coord = 8  # the y grid unit which the mouse is first located in
                self.mouseX = self.x_coord * 20  # calculating the actual pixel value of the mouse's x
                self.mouseY = self.y_coord * 20  # calculating the actual pixel value of the mouse's y
                canvas.create_image(self.mouseX, self.mouseY, image=mouse_image, anchor=NW)  # drawing the first mouse
                self.dir = 0  # setting the direction variable to nothing to start

            # method to update the location of the mouse and draw the cheese & the mouse at the updated location
            def update(self):
                if self.dir == 1:    # moving up
                    self.mouseY = self.mouseY + 20
                elif self.dir == 2:  # moving right
                    self.mouseX = self.mouseX + 20
                elif self.dir == 3:  # moving down
                    self.mouseY = self.mouseY - 20
                elif self.dir == 4:  # moving left
                    self.mouseX = self.mouseX - 20
                canvas.delete(ALL)  # wipes the canvas of all objects
                canvas.create_rectangle(-10, -10, (size * 21), (size * 21), fill="black")  # creates a black background
                canvas.create_image(cheese.cheeseX, cheese.cheeseY, image=cheese_image, anchor=NW)  # draws the cheese
                canvas.create_image(self.mouseX, self.mouseY, image=mouse_image, anchor=NW)  # draws the mouse
                for v in range(0, size):  # draw the white lines which create the grid
                    canvas.create_line((v * 20), 0, (v * 20), (size * 20), fill="white")
                    canvas.create_line(0, (v * 20), (size * 20), (v * 20), fill="white")

        # the cheese class
        class Cheese:
            # initializer method to set the first values of the cheese & create the variables needed
            def __init__(self, cheese_canvas):
                self.canvas = cheese_canvas
                self.x_coord = 1  # the x grid unit which the cheese stays in
                self.y_coord = 1  # the y grid unit which the cheese stays in
                self.cheeseX = self.x_coord * 20  # calculating the actual pixel value for the cheese's x
                self.cheeseY = self.y_coord * 20  # calculating the actual pixel value for the cheese's x
                canvas.create_image(self.cheeseX, self.cheeseY, image=cheese_image, anchor=NW)  # draws the cheese

        # the class for the various obstacles
        class Obstacles:
            # initializer method to set the various obstacles coordinates and draw them
            def __init__(self, obstacle_canvas):
                self.canvas = obstacle_canvas
                self.x1_coord = 2  # obstacle 1's x grid coordinate
                self.y1_coord = 3  # obstacle 1's y grid coordinate
                self.obstacle1X = self.x1_coord * 20  # obstacle 1's actual pixel location for the x coordinate
                self.obstacle1Y = self.y1_coord * 20  # obstacle 1's actual pixel location for the y coordinate
                canvas.create_image(self.obstacle1X, self.obstacle1Y, image=bomb_image, anchor=NW)
                self.x2_coord = 3  # obstacle 2's x grid coordinate
                self.y2_coord = 2  # obstacle 2's y grid coordinate
                self.obstacle2X = self.x2_coord * 20  # obstacle 2's actual pixel location for the x coordinate
                self.obstacle2Y = self.y2_coord * 20  # obstacle 2's actual pixel location for the y coordinate
                canvas.create_image(self.obstacle2X, self.obstacle2Y, image=bomb_image, anchor=NW)
                self.x3_coord = 4  # obstacle 3's x grid coordinate
                self.y3_coord = 1  # obstacle 3's y grid coordinate
                self.obstacle3X = self.x3_coord * 20  # obstacle 3's actual pixel location for the x coordinate
                self.obstacle3Y = self.y3_coord * 20  # obstacle 3's actual pixel location for the y coordinate
                canvas.create_image(self.obstacle3X, self.obstacle3Y, image=bomb_image, anchor=NW)
                self.x4_coord = 1  # obstacle 4's x grid coordinate
                self.y4_coord = 4  # obstacle 4's y grid coordinate
                self.obstacle4X = self.x4_coord * 20  # obstacle 4's actual pixel location for the x coordinate
                self.obstacle4Y = self.y4_coord * 20  # obstacle 4's actual pixel location for the y coordinate
                canvas.create_image(self.obstacle4X, self.obstacle4Y, image=bomb_image, anchor=NW)

            # the method to re-draw the obstacles when necessary
            def draw(self):
                canvas.create_image(self.obstacle1X, self.obstacle1Y, image=bomb_image, anchor=NW)  # draw obstacle 1
                canvas.create_image(self.obstacle2X, self.obstacle2Y, image=bomb_image, anchor=NW)  # draw obstacle 2
                canvas.create_image(self.obstacle3X, self.obstacle3Y, image=bomb_image, anchor=NW)  # draw obstacle 3
                canvas.create_image(self.obstacle4X, self.obstacle4Y, image=bomb_image, anchor=NW)  # draw obstacle 4
                for v in range(0, size):  # draw the white lines which create the grid
                    canvas.create_line((v * 20), 0, (v * 20), (size * 20), fill="white")
                    canvas.create_line(0, (v * 20), (size * 20), (v * 20), fill="white")

        # the method which chooses the next direction for the mouse and implements the Q-Learning algorithm
        def choose_dir():
            max_values = []  # array to contain all of the max Q table values
            new_position = 0  # create a variable to hold the value of the next state
            # create a 4 digit variable to hold the value of the current state ([cheeseX][cheeseY][mouseX][mouseY])
            position = (mouse.mouseX / 20) + ((mouse.mouseY / 20) * size) + (((cheese.cheeseX / 20) * size) * size) + \
                       ((((cheese.cheeseY / 20) * size) * size) * size)
            # set a variable to the max of the 4 Q table values at the current state
            direction = max(QTable[int(position)][0], QTable[int(position)][1], QTable[int(position)][2],
                            QTable[int(position)][3])
            if QTable[int(position)][0] == direction:  # if the max val is equal to the up value add it to the array
                max_values = numpy.append(max_values, ['up'], axis=0)
            if QTable[int(position)][1] == direction:  # if the max val is equal to the right value add it to the array
                max_values = numpy.append(max_values, ['right'], axis=0)
            if QTable[int(position)][2] == direction:  # if the max val is equal to the down value add it to the array
                max_values = numpy.append(max_values, ['down'], axis=0)
            if QTable[int(position)][3] == direction:  # if the max val is equal to the left value add it to the array
                max_values = numpy.append(max_values, ['left'], axis=0)
            # chose a random value from all of the maximum direction in the array we have just appended to
            going = random.choice(max_values)
            if going == 'up':  # if the chosen direction is up change the mouses dir. and change the new position
                mouse.dir = 1
                new_position = position + size
            if going == 'right':  # if the chosen direction is right change the mouses dir. and change the new position
                mouse.dir = 2
                new_position = position + 1
            if going == 'down':  # if the chosen direction is down change the mouses dir. and change the new position
                mouse.dir = 3
                new_position = position - size
            if going == 'left':  # if the chosen direction is left change the mouses dir. and change the new position
                mouse.dir = 4
                new_position = position - 1
            # if the mouse if currently at the cheese, set the reward value to 500
            if mouse.mouseX == cheese.cheeseX and mouse.mouseY == cheese.cheeseY:
                reward = 500
            # if the mouse if currently at any of the obstacles, or has gone off screen, set the reward value to -1000
            elif mouse.mouseX > (size * 19 + 6) or mouse.mouseX < -1 or mouse.mouseY > (size * 19 + 6) or mouse.mouseY \
                 < -1 or (mouse.mouseX == obstacles.obstacle1X and mouse.mouseY == obstacles.obstacle1Y) or \
                         (mouse.mouseX == obstacles.obstacle2X and mouse.mouseY == obstacles.obstacle2Y) or \
                         (mouse.mouseX == obstacles.obstacle3X and mouse.mouseY == obstacles.obstacle3Y) or \
                         (mouse.mouseX == obstacles.obstacle4X and mouse.mouseY == obstacles.obstacle4Y):
                reward = -1000
            # if neither of the above have occurred, set the reward value to -2 just for moving
            else:
                reward = -2
            # use the Q learning algorithm to set a new value for the chosen state based on the current reward, the
            # learning rate, the discount rate, and the next position
            QTable[int(position)][mouse.dir - 1] = (QTable[int(position)][mouse.dir - 1]) + (learningRate *
                                                   (reward + (discountRate * max(QTable[int(new_position)][0],
                                                                                 QTable[int(new_position)][1],
                                                                                 QTable[int(new_position)][2],
                                                                                 QTable[int(new_position)][3]))
                                                                                 - (QTable[int(position)]
                                                                                 [mouse.dir - 1])))

        cheese = Cheese(canvas)  # this is so that i can reference Cheese() as 'cheese' when used later
        mouse = Mouse(canvas)  # this is so that i can reference Mouse() as 'mouse' when used later
        obstacles = Obstacles(canvas)  # this is so that i can reference Obstacles() as 'obstacles' when used later
        if count == 1:  # if it is the very first iteration, calculate the minimum number of moves to the cheese
            minimumMoves = abs(mouse.x_coord - cheese.x_coord) + abs(mouse.y_coord - cheese.y_coord)

        while not dead:  # while the mouse is not dead (off screen or hit an obstacle)
            mouse.update()  # call the update method in the mouse class
            obstacles.draw()  # call the draw method in the obstacles class
            choose_dir()  # call the choose direction method
            # if the mouse has made over 100 moves (ie. is stuck)
            if moves > 100:
                score = 0  # reset the consecutive-cheeses-found counter
                dead = True  # exit this while loop
                previousMoves = moves  # set the previous moves to the current moves
                moves = 0  # reset the moves for the next iteration
            # if the mouse has reached the cheese
            elif mouse.mouseX == cheese.cheeseX and mouse.mouseY == cheese.cheeseY:
                score = score + 1  # add 1 to the consecutive-cheeses-found counter
                if moves == previousMoves:  # if the previous moves and are same as the correct moves adjust accordingly
                    sameMoves = sameMoves + 1
                else:  # if not reset the consecutive same moves counter
                    sameMoves = 0
                cheeseCount = cheeseCount + 1  # add 1 to the total # of cheese's found
                if moves == minimumMoves:  # if the mouse reached the cheese in the minimum moves, print accordingly
                    print("Iteration #" + str(count) + " is mouse #" + str(cheeseCount) + " to have found the cheese "
                                                                                          "and it did so in the least "
                                                                                          "possible moves")
                else:  # if the mouse simply reached the cheese, print the iteration number and the total cheese count
                    print("Iteration #" + str(count) + " is mouse #" + str(cheeseCount) + " to have found the cheese")
                if not last_run:  # once the last run has been completed and it is set to false, quit the learning loop
                    learning = False
                # if the mouse has found the cheese 10 times in a row, all in the same number of moves, set the refresh
                # speed to 250 milliseconds so the program looks like its moving in slow-motion & set last_run to false
                if score > 9 and sameMoves > 9:
                    refresh = 250
                    last_run = False
                dead = True  # dead is set to true to exit the loop exit the loop
                previousMoves = moves  # set the previous moves to the current moves
                moves = 0  # reset the moves for the next iteration
                for w in range(0, size):  # draw the green lines which create the grid showing success
                    canvas.create_line((w * 20), 0, (w * 20), (size * 20), fill="green")
                    canvas.create_line(0, (w * 20), (size * 20), (w * 20), fill="green")
            # if the mouse either goes off the screen or runs into 1 of the 4 obstacles
            elif mouse.mouseX > (size * 19 + 6) or mouse.mouseX < -1 or mouse.mouseY > (size * 19 + 6) or mouse.mouseY \
                    < -1 or (mouse.mouseX == obstacles.obstacle1X and mouse.mouseY == obstacles.obstacle1Y) or \
                            (mouse.mouseX == obstacles.obstacle2X and mouse.mouseY == obstacles.obstacle2Y) or \
                            (mouse.mouseX == obstacles.obstacle3X and mouse.mouseY == obstacles.obstacle3Y) or \
                            (mouse.mouseX == obstacles.obstacle4X and mouse.mouseY == obstacles.obstacle4Y):
                score = 0  # reset the consecutive-cheeses-found counter
                dead = True  # dead is set to true to exit the loop exit the loop
                previousMoves = moves  # set the previous moves to the current moves
                moves = 0  # reset the moves for the next iteration
                for w in range(0, size):  # draw the red lines which create the grid showing failure
                    canvas.create_line((w * 20), 0, (w * 20), (size * 20), fill="red")
                    canvas.create_line(0, (w * 20), (size * 20), (w * 20), fill="red")
            # if the mouse neither hit an obstacle, went off screen or reached the cheese add 1 to its moves taken
            else:
                moves = moves + 1
            tk.after(refresh)  # pause the simulation for 'refresh' milliseconds
            tk.update_idletasks()  # this and the command below update the entire canvas and allow it to be displayed
            tk.update()
    # once the mouse is done learning:
    finish = time.time()  # stop the timer
    finalTime = finish - start  # calculate the total # of seconds elapsed
    finalTime = finalTime/60  # calculate the minutes elapsed
    finalSeconds = finalTime - math.floor(finalTime)  # calculate the remaining seconds elapsed (in minutes)
    finalSeconds = math.floor(finalSeconds * 60)  # convert this decimal to a rounded amount of seconds
    # print the total number of iterations the mouse made and the # of times it reached the cheese
    print('After ' + str(count - 10) + " iterations, the mouse determined the optimal number of moves to the cheese, "
                                       "which it reached " + str(cheeseCount - 10) + " times")
    # print the time elapsed in minutes and seconds
    print("The simulation terminated after " + str(math.floor(finalTime)) + " minutes and " + str(finalSeconds) +
          " seconds")
    tk.destroy()  # destroy the canvas (force close the window)
    print("Press enter to restart the program or type 'N' to quit")  # prompt the user to either quit or restart
    restartQ = input("")
    if restartQ == "N":  # if they chose to quit, exit the main loop and the program will end
        looping = False
    else:  # if they chose to restart, re-initialize all variables to their starting values
        size = 10
        learningRate = 0.80
        discountRate = 0.70
        score = 0
        minimumMoves = 0
        cheeseCount = 0
        previousMoves = 0
        sameMoves = 0
        moves = 0
        count = 0
        speed = 0
        refresh = 0
        looping = True
        learning = True
        caught = False
        speed_check = True
        last_run = True
        # re-declare the Q table array & fill it completely with 0s using the for loop
        QTable = [[float(0), float(0), float(0), float(0)]]
        for i in range(0, (size * size * size * size)):
            QTable = numpy.append(QTable, [[float(0), float(0), float(0), float(0)]], axis=0)
