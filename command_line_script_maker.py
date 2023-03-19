import os

output_txt_filename = 'command_line.bat'
if not os.path.exists(output_txt_filename):
    with open(output_txt_filename, 'w') as file:
        file.write(r'cd PATH\bad_apple_tetris' + '\n')
        for i in range(0,2589+1):
            file.write(f'python image_processing/ip_main.py {i}'+'\n')