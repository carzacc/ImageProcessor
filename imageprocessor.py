from wand.image import Image
from wand.drawing import Drawing
import os
from sys import argv
from shutil import copyfile

class ImageProcessor:

    def __init__(self, dir, save_dir, process = True):
        self.i = 0
        self.dir = dir
        self.save_dir = save_dir
        self.edit = process

    def process(self, area: os.DirEntry, city: os.DirEntry, pic: os.DirEntry, save_dir: str):
        # os.DirEntry.name is the picture's filename
        filename = pic.name

        # Store the absolute path of the current directory
        # so that we can return to it when we're done,
        # so that the calling function doesn't end up
        # with a working directory that is not the same
        # as the one it had before the call to process()
        return_dir = os.path.abspath(os.curdir)

        # os.path.splitext gives us both the file name and
        # the extension of the picture. We need the extension
        # because we're going to use it to tell Wand
        # (and, in turn, ImageMagick) what extension
        # to give to the image and we want to retain
        # the original one
        (name, extension) = os.path.splitext(pic)
        text = f'{city.name}({area.name})'
        save_name = f'{self.i}-{text}{extension}'

        if self.edit:
            with Image(filename=filename) as image:
                draw = Drawing()
                draw.fill_color = "white"
                draw.font_size = 90
                draw.gravity = "south_east"
                draw.text(30, 30, text)
                draw.draw(image)
                os.chdir(save_dir)
                image.save(filename=save_name)
            self.i=self.i+1
        else:
            copyfile(pic.name, f"{save_dir}/{save_name}")

        os.chdir(return_dir)

    def process_dir(self):
        if len(argv) < 3:
            print("Some arguments are missing.")
            print("Usage: picorganizer.py input_directory output_directory")
            return

        areas = []

        try:
            areas = [file for file in os.scandir(self.dir) if file.is_dir()]
            if len(areas) == 0:
                raise Exception("No subdiretories in input path")
        except:
            print(f"The provided input path \"{self.dir}\" is not valid")

        save_dir = []

        try:
            save_dir = [dir for dir in os.scandir(f"{self.save_dir}/..") if dir.name == os.path.split(self.save_dir)[1] and dir.is_dir()][0]
        except:
            print(f"The provided output path \"{self.save_dir}\" doesn't exist or is invalid")

        for area in areas:
            os.chdir(area)
            cities = [file for file in os.scandir(".") if file.is_dir()]
            for city in cities:
                os.chdir(city)
                pics = [file for file in os.scandir(".") if file.is_file()]
                for pic in pics:
                    self.process(area, city, pic, os.path.abspath(save_dir))
                os.chdir(os.pardir)
            os.chdir(os.pardir)