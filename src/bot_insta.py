from __future__ import unicode_literals
import sys
import os
import argparse
import random
import time
import shutil

from instabot import Bot
from instabot import utils

from generate_image import GenerateImage # generate_image.py
import captions_for_medias # captions_for_medias.py

class BotInsta(object):
    def __init__(self):
        self.current_carpet = os.path.split(os.path.realpath(__file__))[0]
        self.carpet_media = "{}{}".format(self.current_carpet, '/../media/')
        self.carpet_store_files = "{}{}".format(self.current_carpet, '/../store_files/')
        self.bot = Bot(base_path=self.carpet_store_files) # Files created by Bot()

    def login(self, username, password):
        return self.bot.api.login(username, password)

    def check_followers(self):
        followers_list = "{}followers_list.txt".format(self.carpet_store_files)
        followers_log  = "{}followers_log.txt".format(self.carpet_store_files)
        username = self.bot.username

        text_message_new_follower = ("¡Hola! Gracias por empezar a seguirme, espero poder "
                                     " compartirte buenas motivaciones y que cumplás con tu "
                                     "tareas diarias.\n\nTe dejo una imagen de Piolín porque "
                                     "nadie puede odiar a Piolín. Saludos :D")

        text_message_user_unfollow = ("Hey, pareces que dejaste de seguirme, que mal :/\n\nBueno "
                                      "espero verte entre mis likes algún día de nuevo.\n\nTe "
                                      "dejo una imagen de Piolín porque lo hiciste ponerse triste :(")

        path_image_new_follower = "{}images/backgrounds/welcome_follower.jpg".format(self.carpet_media)
        path_image_unfollower = "{}images/backgrounds/goodbye_unfollower.jpg".format(self.carpet_media)

        save_followers = self.save_followers(username, followers_list, followers_log)
        if (save_followers):
            (followers, new_followers, unfollowers) = save_followers
            if(len(new_followers) > 0):
                self.bot.logger.info("There are new followers")
                for user in new_followers:
                    self.send_message_image_new_follower(user, text_message_new_follower, path_image_new_follower)
            if(len(unfollowers) > 0):
                self.bot.logger.info("There are unfollowers")
                for user in unfollowers:
                    self.send_message_image_unfollow(user, text_message_user_unfollow, path_image_unfollower)
        self.bot.logger.info("There are no changes in followers")
        self.bot.logger.info("Check followers finished")
        return True

    # https://github.com/instagrambot/instabot/blob/master/examples/welcome_message.py
    def get_followers(self, username, followers_list):
        self.bot.logger.info("Getting all followers of {}".format(username))
        current_followers = self.bot.get_user_followers(username)
        save_followers = utils.file(followers_list)
        if not save_followers.list:
            save_followers.save_list(current_followers)
            self.bot.logger.info("{} file didn't exist. Creating file".format(followers_list))
            self.bot.logger.info("File {} created".format(followers_list))
            self.bot.logger.info('Followers saved for first time in file {}'.format(followers_list))
            self.bot.logger.info("Get followers has been completed")
            exit(0)

        with open(followers_list, 'r') as f:
            self.bot.logger.info("File {} exist".format(followers_list))
            self.bot.logger.info("Reading followers of the file")
            saved_followers = [x.strip('\n') for x in f.readlines()]

        if (len(current_followers) > 0):
            self.bot.logger.info("Comparing followers saved between current followers")
            new_followers = [x for x in current_followers if x not in saved_followers]
            unfollowers = [x for x in saved_followers if x not in current_followers]
            self.bot.logger.info("Get followers has been completed")
            return (current_followers, new_followers, unfollowers)
        self.bot.logger.info("Error. Problem with connection. No followers returned")
        return (saved_followers, [], [])
    
    def save_followers(self, username, followers_list, followers_log):
        self.bot.logger.info("Saving all followers in log file {}".format(followers_log))
        datetime = time.strftime("%d-%m-%Y %H:%M:%S")
        (followers, new_followers, unfollowers) = self.get_followers(username, followers_list)
        lines = []
        with open(followers_log, 'a') as file:
            lines.append("===================================\n")
            lines.append(datetime + "\n")
            lines.append("===================================\n")
            lines.append("News: {}\n".format(len(new_followers)))
            lines.append("-----\n")
            for new in new_followers:
                lines.append(new + "\n")
            lines.append("------------------\n")
            lines.append("Unfollow me: {}\n".format(len(unfollowers)))
            lines.append("-----\n")
            for unfollow in unfollowers:
                lines.append(unfollow + "\n")
            lines.append("------------------\n")
            lines.append("Total: {}\n".format(len(followers)))
            lines.append("-----\n")
            for follow in followers:
                lines.append(follow + "\n")

            for item in lines:
                file.write(item)
            followers_list = utils.file(followers_list)
            followers_list.save_list(followers)
            return (followers, new_followers, unfollowers)
        return False

    def send_message_image_new_follower(self, userid, message, image):
        self.bot.logger.info("Sending message to new follower {}".format(userid))
        self.bot.logger.info("Sending image {}".format(image))
        if (self.bot.send_photo(userid, image)):
            self.bot.logger.info("Image sent")
            self.bot.logger.info("Sending message text")
            if (self.bot.send_message(message, userid)):
                self.bot.logger.info("Message text sent")
                self.bot.logger.info("Finish message process")
                return True
            else:
                return False
        else:
            return False
        return False
    
    def send_message_image_unfollow(self, userid, message, image):
        self.bot.logger.info("Sending message to unfollower user {}".format(userid))
        self.bot.logger.info("Sending image {}".format(image))
        if (self.bot.send_photo(userid, image)):
            self.bot.logger.info("Image sent")
            self.bot.logger.info("Sending message text")
            if (self.bot.send_message(message, userid)):
                self.bot.logger.info("Message text sent")
                self.bot.logger.info("Finish message process")
                return True
            else:
                return False
        else:
            return False
        return False

    def send_message_all_followers(self):
        followers_list = "{}followers_list.txt".format(self.carpet_store_files)
        text_message = "Hi :)"
        path_image = "{}images/backgrounds/welcome_follower.jpg".format(self.carpet_media)

        with open(followers_list, 'r') as f:
            self.bot.logger.info("File {} exist".format(followers_list))
            self.bot.logger.info("Reading followers of the file")
            saved_followers = [x.strip('\n') for x in f.readlines()]

        for user in saved_followers:
            self.send_message_image_new_follower(user, text_message, path_image)
        return True

    def send_message_after_publication(self, type_img="photo", to_username=None, text_message=None):
        datetime = time.strftime("%d/%b/%Y %H:%M:%S")
        text_message = text_message.format(datetime)
        self.bot.logger.info("Sending message to master {} about last {} published ".format(to_username, type_img))
        self.bot.logger.info("Text of message {}".format(text_message))
        if (type_img == "photo"):
            last_publication_id = self.bot.get_last_user_medias(self.bot.username, 1)
            self.bot.logger.info("Last publication ID {}".format((last_publication_id[0])))
            return self.bot.send_media(last_publication_id[0], to_username, text_message)
        else:
            return self.bot.send_message(text_message, to_username)

    def get_text_publication(self, type_text="photo"):
        self.bot.logger.info("Get publication text for type {}".format(type_text))
        index_caption = random.randint(0, (len(captions_for_medias.TEXTS_PUBLICATION[type_text])) - 1)
        self.bot.logger.info("Index of the text selected is: {}".format(index_caption))
        username = self.bot.username
        date = time.strftime("%d/%b/%Y")
        caption = (captions_for_medias.TEXTS_PUBLICATION[type_text])[index_caption]
        caption = caption.format(motivador=username, date=date)
        self.bot.logger.info("Selected text to the publication is: {}".format(caption))
        return caption

    def get_text_quote(self, type_text="photo"):
        self.bot.logger.info("Get text quote for type {}".format(type_text))
        index_caption = random.randint(0, (len(captions_for_medias.QUOTES_PUBLICATION[type_text])) - 1)
        self.bot.logger.info("Index of the quote selected is: {}".format(index_caption))
        caption = (captions_for_medias.QUOTES_PUBLICATION[type_text])[index_caption]
        self.bot.logger.info("Selected text to the quote is: {}".format(caption))
        return caption

    def make_publication_photo(self, username_master, text_message_to_master):
        self.generator_img = GenerateImage(self.bot)
        self.bot.logger.info("=========================================")
        self.bot.logger.info("==== Publishing Photo into Timeline =====")
        self.bot.logger.info("=========================================")
        try:
            type_img = "photo"
            self.bot.logger.info("Generating publication of type {}".format(type_img))
            text_publication = self.get_text_publication(type_img)
            relative_path_img = self.generate_image(type_img)
            self.bot.logger.info("Upload image {}".format(relative_path_img))
            if not self.bot.api.upload_photo(relative_path_img, text_publication, None, None, False, ({'rename': False})):
                self.bot.logger.error("Something went wrong in update photo for publication")
            else:
                self.bot.logger.info("Current path: {}".format(relative_path_img))
                if (self.generator_img.remove_published_image(type_img, relative_path_img)):
                    self.bot.logger.info("Publication on Instagram is completed")
                    self.bot.logger.info("Now preparing to send message to master @{}".format(username_master))
                    if (self.send_message_after_publication(type_img, username_master, text_message_to_master)):
                        self.bot.logger.info("Message sent to master")
                        self.bot.logger.info("Finish process of publication")
        except Exception as e:
            self.bot.logger.error(str(e))
    
    def make_publication_story(self, username_master, text_message_to_master):
        self.bot.logger.info("=========================================")
        self.bot.logger.info("=========== Publishing Story ============")
        self.bot.logger.info("=========================================")
        try:
            type_img = "story"
            self.bot.logger.info("Generating publication of type {}".format(type_img))
            text_publication = self.get_text_publication(type_img)
            relative_path_img = self.generate_image(type_img)
            self.bot.logger.info("Upload image {}".format(relative_path_img))
            if not self.bot.api.upload_story_photo(relative_path_img):
                self.bot.logger.error("Something went wrong in update story photo")
            else:
                self.bot.logger.info("Current path: {}".format(relative_path_img))
                if (self.generator_img.remove_published_image(type_img, relative_path_img)):
                    self.bot.logger.info("Publication on Instagram is completed")
                    self.bot.logger.info("Now preparing message to master @{}".format(username_master))
                    if (self.send_message_after_publication(type_img, username_master, text_message_to_master)):
                        self.bot.logger.info("Message sent to master")
                        self.bot.logger.info("Finish process of publication")

        except Exception as e:
            self.bot.logger.error(str(e))

    def generate_image(self, type_img):
        self.generator_img = GenerateImage(self.bot)
        quote_publication = self.get_text_quote(type_img)
        return self.generator_img.draw_image(type_img, quote_publication)
