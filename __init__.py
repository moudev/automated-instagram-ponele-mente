import schedule
import time
import os
import sys
import threading

sys.path.append(os.path.join(sys.path[0], './src'))
from bot_insta import BotInsta

# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

def check_server():
    """ Checks server status """
    datetime = time.strftime("%d/%b/%Y %H:%M:%S")
    print("[{}] I'M STILL ALIVE".format(datetime))

def job_after_server_init(params):
    """Execute a function only one time

    Parameters:
        params (tuple): [0] contains function to execute
            and [1:] params of the functions
    """
    print("====================================")
    print("===== Executed only one time =======")
    print("====================================")
    ejecutar = params[0]
    (master_username, text_message) = params[1:]
    ejecutar(master_username, text_message)
    return schedule.CancelJob

def run_threaded(params):
    """Execute a function only one time

    Parameters:
        params (tuple): [0] contains function to execute
            and [1:] params of the functions
    """
    print("====================================")
    print("I'm running on thread %s" % threading.current_thread())
    job_thread = threading.Thread(target=params[0], args=params[1:])
    job_thread.start()

# https://medium.com/dataseries/hiding-secret-info-in-python-using-environment-variables-a2bab182eea
username = os.environ.get('username')
password = os.environ.get('password')

# username that will receive notifications about posts
master_username = os.environ.get('master_username')
# message text of the notifications
text_message_photo = "{}\n\nwasup! Master, quiondas, mirá, acabo de hacer ésta publicación.\n\n========="
text_message_story = "{}\n\nwasup! Master, quiondas, mirá, acabo de publicar una historia.\n\n=========="

bot = BotInsta()
bot.login(username, password)

# https://schedule.readthedocs.io/en/stable/
schedule.every().minute.do(check_server)

""" Check bot_insta.py. Line 49 and 52 """
# schedule.every(30).minutes.do(bot.check_followers)
schedule.every(5).to(10).minutes.do(job_after_server_init,( bot.make_publication_photo, master_username, text_message_photo ))
schedule.every(20).to(30).minutes.do(job_after_server_init,( bot.make_publication_story, master_username, text_message_story ))
schedule.every(6).to(7).hours.do(run_threaded,( bot.make_publication_photo, master_username, text_message_photo ))
schedule.every(4).to(5).hours.do(run_threaded,( bot.make_publication_story, master_username, text_message_story ))

while True:
    schedule.run_pending()
    time.sleep(1)
