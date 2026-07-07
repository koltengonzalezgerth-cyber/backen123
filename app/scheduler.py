"""
Runs the ingestion cycle on a recurring interval inside the same process
as the API server. For higher-traffic production use, run this as a
separate worker process/cron job instead of inside the API process.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.ingestion.run_ingest import run_ingest_cycle

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        run_ingest_cycle,
        "interval",
        minutes=settings.INGEST_INTERVAL_MINUTES,
        next_run_time=None,  # don't fire immediately on boot; first run is scheduled
        id="ingest_cycle",
        replace_existing=True,
        max_instances=1,       # never run two ingestion cycles concurrently
        coalesce=True,         # if a run was missed (e.g. process was asleep), run once, not N times
        misfire_grace_time=120,
    )
    scheduler.start()
