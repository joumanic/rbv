from brand import RadioBuenaVida

class EventHandler:
    def __init__(self):
        self.rbv = RadioBuenaVida()
    
    def handle_event(self, event):
        if event.get("trigger"):
            self.rbv.create_social_media_assets()

            return {"statusCode": 200, "body": "Successful Event"}
        else:
            return {"statusCode": 300, "body": "Not Triggered"}


