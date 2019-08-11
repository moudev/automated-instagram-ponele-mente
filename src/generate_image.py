from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import logging
import os
import time
import shutil

class GenerateImage(object):
    def __init__(self, bot=None):
        self.logger = logging
        self.username = ""
        if (bot != None):
            self.logger = bot.logger
            self.username = bot.username
        self.carpet = os.path.split(os.path.realpath(__file__))[0]

    def get_background_image(self, type_img="photo"):
        self.logger.info("Getting background for {}".format(type_img))
        image = ''
        if (type_img == "photo"):
            image = "photo_background.jpg"
        else:
            image = "story_background.jpg"
        path_background = "{}/../media/images/backgrounds/{}".format(self.carpet, image)
        self.logger.info("Path restul for background: {}".format(path_background))
        return path_background

    def get_path_to_save_image(self, type_img="photo"):
        self.logger.info("Getting published carpet for: {}".format(type_img))
        carpet = ''
        if (type_img == "photo"):
            carpet = "photos"
        else:
            carpet = "stories"
        self.logger.info(os.path.basename(__file__)+"../media/images/published/{}".format(carpet))
        return os.path.basename(__file__)+"../media/images/published/{}".format(carpet)

    def get_position_text_image(self, type_img="photo"):
        # t = title, q = quote, d = date, u = username, n = note
        (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        if (type_img == "photo"):
            # 1000px
            (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn) = (264, 168, 89, 373, 831, 878, 787, 914, 692, 948)
            # 600px
            # (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn) = (158, 103, 50, 226, 499, 526, 472, 547, 413, 569)
        else:
            (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn) = (325, 175, 100, 450, 747, 1650, 673, 1700, 519, 1753)
        return (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn)

    def get_font_size_text_image(self, type_img="photo"):
        # t = title, q = quote, d = date, u = username, n = note
        (ft, fq, fn) = (0, 0, 0)
        if (type_img == "photo"):
            # 1000px
            (ft, fq, fn) = (72, 109, 25)
            # 600px
            # (ft, fq, fn) = (43, 66, 15)
        else:
            (ft, fq, fn) = (71, 87, 45)
        return (ft, fq, fn)

    # https://haptik.ai/tech/putting-text-on-images-using-python-part2/
    def text_wrap(self,text, font, max_width):
        lines = []
        if font.getsize(text)[0] <= max_width:
            lines.append(text) 
        else:
            words = text.split(' ')  
            i = 0
            while i < len(words):
                line = ''         
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)    
        return lines

    def draw_image(self, type_img="photo", quote="Example quote"):
        try:
            path_image = self.get_background_image(type_img)
            self.logger.info("Returned background: {}".format(path_image))
            if (os.path.isfile(path_image)):
                self.logger.info("Getting background")
                image = Image.open(path_image)
                (max_width, max_height) = image.size

                draw = ImageDraw.Draw(image)

                color = "rgb(255, 255, 255)" # White color

                date = time.strftime("%d/%b/%Y")
                username = "@{}".format(self.username)
                note = "Soy un IG semi-autónomo"

                (xt, yt, xq, yq, xd, yd, xu, yu, xn, yn) = self.get_position_text_image(type_img)
                (ft, fq, fn) = self.get_font_size_text_image(type_img)

                self.logger.info("Getting text positions")
                font_carpet = "{}/../fonts/Avenir-Roman.ttf".format(self.carpet)
                font_title = ImageFont.truetype(font_carpet, size=ft)
                font_quote = ImageFont.truetype(font_carpet, size=fq)
                font_note = ImageFont.truetype(font_carpet, size=fn)

                self.logger.info("Getting font-sizes")
                
                draw.text((xt, yt), "¡Ponele Mente!", fill=color, font=font_title)
                draw.text((xd, yd), date, fill=color, font=font_note)
                draw.text((xu, yu), username, fill=color, font=font_note)
                draw.text((xn, yn), note, fill=color, font=font_note)

                self.logger.info("Drawing texts")
                
                lines_wrap = self.text_wrap(quote, font_quote, (max_width - (xq * 2))) # Add padding
                line_height = font_quote.getsize('hg')[1]
                for line in lines_wrap:
                    draw.text((xq, yq), line, fill=color, font=font_quote)
                    yq = yq + line_height

                datetime_img = time.strftime("%d%b%Y_%H%M%S")
                name_img = "{}_{}.jpg".format(type_img, datetime_img)
                path_tmp = "{}/../media/images/tmp/{}".format(self.carpet, name_img)

                self.logger.info("Saving image in path: {}".format(path_tmp))

                image.save(path_tmp)
                self.logger.info("Image saved")
                return path_tmp
            else:
                raise Exception("{path_image} not existed".format(path_image))
        except Exception as e:
            self.logger.error("\033[41mERROR...\033[0m")
            self.logger.error(str(e))

    def move_published_image(self, type_img, current_path):
        filename = os.path.basename(current_path)
        destination_path = self.get_path_to_save_image(type_img)
        self.logger.info("destination path: {}".format(destination_path))
        final_destination = "{}/{}".format(destination_path, filename)
        absolute_final_destination = os.path.dirname(os.path.realpath(__file__)) + "/" +final_destination
        self.logger.info("Destination path: {}".format(absolute_final_destination))
        shutil.move(current_path, absolute_final_destination)
        return True

    def remove_published_image(self, type_img, current_path):
        self.logger.info("Removing file: {}".format(current_path))
        if (type_img == "story"):
            os.remove(current_path)
            current_path = current_path + ".STORIES.jpg"
        os.remove(current_path)
        self.logger.info("Removed file: {}".format(current_path))
        return True
