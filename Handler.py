import os
from pathlib import Path
from shutil import copyfile


class Handler:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.input_directory = self.root_directory + '/Input/'
        self.output_directory = self.root_directory + '/Output/'
        self.temp_directory = self.root_directory + '/Temp/'
        self.video_name = ''
        self.frames_list = []
        self.start_program()

    def start_program(self):
        if os.path.exists(self.input_directory):
            pass
        else:
            os.mkdir('Input')

        os.chdir(self.root_directory)

        if os.path.exists(self.output_directory):
            pass
        else:
            os.mkdir('Output')

        os.chdir(self.root_directory)

        if os.path.exists(self.temp_directory):
            pass
        else:
            os.mkdir('Temp')

        os.chdir(self.root_directory)

    def find_video_name(self):
        video_name = os.listdir(self.input_directory)
        return video_name[0]

    def clear_temp(self):
        os.chdir(self.root_directory)
        names = os.listdir(self.temp_directory)
        for file in names:
            os.remove(self.temp_directory + file)
        os.chdir(self.root_directory)

    def save(self):
        names = os.listdir(self.temp_directory)
        for i in names:
            copyfile(self.temp_directory + i, self.output_directory + i)

        os.chdir(self.root_directory)
        names = os.listdir(self.temp_directory)
        for file in names:
            os.remove(self.temp_directory + file)
        os.rmdir(self.temp_directory)
