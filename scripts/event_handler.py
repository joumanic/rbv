from brand import RadioBuenaVida
import logging

class EventHandler:
    def __init__(self):
        self.rbv = RadioBuenaVida()
    
    def handle_event(self, event):
        if event == "create social media assets":
            logging.info("Create Show Social Media Assets Task Started")
            self.rbv.create_show_social_media_assets()
            logging.info("Finished Create Social Media Assets Event")
        elif event ==  "create monthly color assets":
            logging.info("Create Monthly Assets Task Started")
            self.rbv.create_monthly_colors_assets()
            logging.info("Finished Create Monthly Color Assets Event")
        else :
            logging.info({"statusCode": 300, "body": "Not Triggered"})


