from apscheduler.schedulers.background import BackgroundScheduler
from decorators.service import service
import atexit
from services.discord import DiscordService

@service()
class SchedulerService():
    
    discord_service = DiscordService.get_instance()
    _scheduler = None

    def create_jobs(self):
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(func=self.discord_service.update_repo, trigger="interval", seconds=10)
        self._scheduler.add_job(func=self.discord_service.has_new_messages, trigger="interval", seconds=10)
        self._scheduler.start()
        atexit.register(lambda: self._scheduler.shutdown())

    def wait_for_jobs(self):
        while self._scheduler and self._scheduler.running:
            pass

