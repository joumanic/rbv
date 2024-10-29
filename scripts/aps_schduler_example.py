from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def scheduled_task():
    print(f"Task executed at {datetime.now()}")

if __name__ == '__main__':
    scheduler = BlockingScheduler()

    # Schedule a job to run every minute
    scheduler.add_job(scheduled_task, 'interval', minutes=1)

    print("Scheduler started. Waiting for tasks...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
