from event_handler import EventHandler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz


if __name__ == "__main__":
    handler = EventHandler()
    scheduler = BlockingScheduler(timezone=pytz.UTC)
    handler.handle_event("create social media assets")

    scheduler.add_job(lambda:handler.handle_event("create social media assets"), 'cron', day_of_week='sat', hour=12, minute=0)

    scheduler.add_job(lambda:handler.handle_event("create monthly color assets"), 'cron', day=1, hour=12, minute=0)

    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass