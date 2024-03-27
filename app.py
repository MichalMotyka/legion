from services.gemini import GeminiService
from services.discord import DiscordService
from services.scheduler import SchedulerService

gemini_service = None

if __name__ == '__main__':
    gemini_service = GeminiService.get_instance()
    discord_service = DiscordService.get_instance()
    SchedulerService.get_instance().create_jobs()
    discord_service.update_repo()
    SchedulerService.get_instance().wait_for_jobs()