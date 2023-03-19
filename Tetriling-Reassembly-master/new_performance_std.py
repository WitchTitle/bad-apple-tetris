# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: PERFORMANCE TEST
# Authors: Liuqing Chen, Feng Shi, and Isaac Engel
# Last updated: 25th July 2018
# ####################################################

from main import Tetris
import utils
import timeit
from copy import deepcopy
import numpy as np

# Example target shape, limit_tetris, and perfect_solution
target = [
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1]
         ]

# target = [
#             [0, 0, 1, 0, 0, 1],
#             [0, 0, 1, 1, 1, 1],
#             [0, 1, 1, 1, 1, 1],
#             [0, 1, 1, 1, 0, 1],
#             [1, 1, 1, 1, 1, 0]
#          ]
target = [[1]*30]*30

import sys
sys.path.insert(1, 'bad_apple_tetris/image_processing/ip_main')
sys.path.insert(1, r'C:\Users\demor\OneDrive\Documents\python_scripts\bad_apple_tetris\image_processing')

from ip_main import array_source

#target = array_source
         
limit_tetris = {1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 1, 14: 0, 15: 0, 16: 0, 17: 0, 18: 1, 19: 0}

limit_tetris = {x:len(target)*len(target[0]) for x in range(1, 20)} #19 for the 19 different orientations of 7 tetrominos
#limit_tetris = {x:0 for x in range(1, 20)} #19 for the 19 different orientations of 7 tetrominos
#limit_tetris[19] = len(target)*len(target[0])

# 1 is square
# 2 is vertical I
# 3 is horizontal I
# 4 is L
# 5 is left L
# 6 is upsidedown L
# 7 is right L
# 8 is J
# 9 is left J
# 10 is upsidedown J
# 11 is right J
# 12 is left T
# 13 is upsidedown T
# 14 is right T
# 15 is T
# 16 is S
# 17 is left S
# 18 is Z
# 19 is left Z


#limit_tetris = {x:1 for x in range(1,i)}

# perfect_solution = [
#                     [(0, 0),  (0, 0),  (8, 1),  (0, 0),   (0, 0)],
#                     [(0, 0),  (0, 0),  (8, 1),  (1, 2),   (1, 2)],
#                     [(0, 0),  (8, 1),  (8, 1),  (1, 2),   (1, 2)],
#                     [(0, 0),  (13, 3), (18, 4), (18, 4),  (0, 0)],
#                     [(13, 3), (13, 3), (13, 3), (18, 4),  (18, 4)]
#                 ]
# NOTE: This example is used for the mock solution from 'main.py' only.

# Uncomment the following line to generate a random target shape
#target, limit_tetris, perfect_solution = utils.generate_target(width=20, height=20, density=0.8)  # NOTE: it is recommended to keep density below 0.8

solution = Tetris(deepcopy(target),deepcopy(limit_tetris))
print('oof')
print(np.array(solution).shape)
for x in solution:
    print(x)
    print()
print('oof')

valid, missing, excess, error_pieces, use_diff = utils.check_solution(target, solution, limit_tetris)  # checks if the solution is valid

if not valid or len(error_pieces)!=0:
    if len(error_pieces) != 0:
        print('WARNING: {} pieces have a wrong shapeID. They are labelled in image of the solution, and their PieceID are: {}.'
                .format(len(error_pieces), error_pieces))
        print("Displaying solution...")
        #utils.visual_perfect(perfect_solution, solution)
    print("WARNING: The solution is not valid, no score will be given!")

else:  # if the solution is valid, test time performance and accuracy

    # TIME PERFORMANCE
    # There will be three different 'target' with increasing complexity in real test.

    time_set = timeit.timeit('Tetris({},{})'.format(target,limit_tetris), 'from main import Tetris', number=1)
    
    if time_set > 600:

        print("WARNING: Time is over 10 minutes! The solution is not valid")

    else:

        print("Time performance")
        print("----------------")
        print("The running time was {:.5f} seconds.\n".format(time_set))

        # ACCURACY

        print("Accuracy")
        print("--------")

        print('All pieces are labelled with correct shapeID and pieceID.')
        if len(use_diff)==0:
            print ('All given Tetris have been fully used.')
        else:
            print("The difference of Tetris usage between task and solution: \n\t",use_diff,"\n")

        total_blocks = sum([sum(row) for row in target])
        total_blocks_solution = total_blocks - missing + excess

        print("The number of blocks in the TARGET is {:.0f}.".format(total_blocks))
        print("The number of blocks in the SOLUTION is {:.0f}.".format(total_blocks_solution))
        print("There are {} MISSING blocks ({:.4f}%) and {} EXCESS blocks ({:.4f}%).\n".format
            (missing, 100 * missing / total_blocks, excess, 100 * excess / total_blocks))

        # VISUALISATION
        # NOTE: for large sizes (e.g., 100x100), visualisation will take several seconds and might not be that helpful.
        # Feel free to comment out the following lines if you don't need the visual feedback.

        #print("Displaying solution...")
        #utils.visual_perfect(solution, solution)
        utils.visualisation(target, solution)



