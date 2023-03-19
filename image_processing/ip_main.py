import os, sys
from PIL import Image, ImageDraw
from tqdm import tqdm
import numpy as np
from time import perf_counter


sys.path.insert(1, r'C:\Users\demor\OneDrive\Documents\python_scripts\bad_apple_tetris\Tetriling-Reassembly-master')
sys.path.insert(1, r'C:\Users\demor\OneDrive\Documents\python_scripts\bad_apple_tetris\image_processing')

from main import Tetris
from utils import check_solution


tetromino_index_to_shape = {1:'O', 2:'I', 3:'I', 4:'L', 5:'L', 6:'L', 7:'L', 8:'J', 9:'J', 10:'J', 11:'J', \
                         12:'T', 13:'T', 14:'T', 15:'T', 16:'S', 17:'S', 18:'Z', 19:'Z'}

for i in range(1,len(tetromino_index_to_shape)+1):
    letter = tetromino_index_to_shape[i]
    block = Image.open(f'image_processing/block_images/{letter}_block.png').convert('RGB')
    tetromino_index_to_shape[i] = block


block_width, block_height = block.size
print(block.size)
apple_num_frames = 2589 #the bad apple rendered in 15 fps has 2589 frames
#apple_num_frames = 100

main_board = Image.new('RGB', (1920, 1080))


end_folder = "image_processing/end/"
if not os.path.exists(end_folder):
   os.makedirs(end_folder)

print("Rendering...")
#for k in tqdm(range(apple_num_frames)):

start_frame_index = int(sys.argv[1])
end_frame_index = start_frame_index + 1
if end_frame_index > apple_num_frames:
    end_frame_index = apple_num_frames

for k in tqdm(range(start_frame_index, end_frame_index)): #for each frame


    board = main_board


    b = len(str(k))-1 #1-9 returns 0, 10-99 returns 1, 100-999 returns 2...
    zero = "0"*(5-b) #Sony vegas image sequences are name_000000
    name = "a_"+zero + str(k) #an example of name is a_000123 (frame 123)

    source = Image.open("image_processing/apple/"+name+".jpeg").convert("L") #the source image in black and white

    #pixelate image 
    source = source.resize((1920//36,1080//36), resample=Image.BILINEAR)
    #print(source.size)
    binarized_source_image = source.point(lambda x: 255 * (x > 128))
    binarized_source_for_array = source.point(lambda x: 1 * (x > 128))
    
    array_source = np.asarray(binarized_source_for_array).tolist()
    #print(array_source)
    # Scale back up using NEAREST to original size
    big_source = source.resize( (1920, 1080), Image.NEAREST)
    big_source = binarized_source_image.resize( (1920, 1080), Image.NEAREST)


    #big_source.save('image_processing/end/'+name+'.jpg')
    #big_source.save('image_processing/test_end/'+name+''+'.jpg')

    t1_start = perf_counter()

    valid = False
    while not valid:
        limit_tetris = {x: sum(row.count(1) for row in array_source) / (4*6) for x in range(1, 20)}
        tetris_solution = Tetris(array_source, limit_tetris)
        if tetris_solution == None:
            valid = True
            break
        valid, missing, excess, error_pieces, use_diff = check_solution(array_source, tetris_solution, limit_tetris)
        if perf_counter() - t1_start > 15:
            tetris_solution = None
            valid = True
            break


    if tetris_solution == None:
        board = board.convert('RGB')
        board.save('image_processing/end/'+name+'.jpg')
        #board.save('image_processing/test_end/'+name+'.jpg')
        continue

    #print('tetris solution:')
    #print(tetris_solution)



    for i in range(source.width):
        for j in range(source.height):
            try:
                tetromino_index = tetris_solution[j][i][0]
            except:
                raise Exception(f'i j = {i} {j} source size = {source.size} \
                                tetris soln size = {len(tetris_solution)} {len(tetris_solution[0])} \
                                tetromino index is {tetromino_index}')
            if tetromino_index != 0:
                board.paste(tetromino_index_to_shape[tetromino_index], ( i*36 , j*36 ))

    board = board.convert('RGB')
    board.save('image_processing/end/'+name+'.jpg')
    #board.save('image_processing/test_end/'+name+'.jpg')


print("Done!")
