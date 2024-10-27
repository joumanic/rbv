from file_handler import FileHandler
from image_processor import ImageProcessor
from brand import RadioBuenaVida

from dropbox.services.files import DropboxService

POST_SQUARE_SIZE= 1080
FONT_SHOW_SIZE_RATIO = 0.04
FONT_GENRE_SIZE_RATIO = 0.035
SHOW_TEXT = "David Barbarossa's Simple Food"
GENRE_TEXT_TEST = "Disco | Boogie | Leftfield"

class EventHandler:
    def __init__(self):
        self.rbv = RadioBuenaVida()
    
    def handle_event(self, event):
        if event.get("trigger"):
            self.rbv.create_social_media_assets()

            return {"statusCode": 200, "body": "Successful Event"}
        else:
            return {"statusCode": 300, "body": "Not Triggered"}


