import asyncio
import os
import uuid
from datetime import datetime
from time import time

import prometheus_client

from prozorro_sale import metrics
from prozorro_sale.tools import logger
from prozorro_sale.tools.logger import REQUEST_ID


LOG = logger.get_custom_logger(__name__)
KEEP_RUNNING = True
# number of seconds to protect procedure from other workers
PROCESSING_LOCK = os.getenv('PROCESSING_LOCK', 1)
time_tick = prometheus_client.Summary('chronograph_tick_latency', 'Time to tick')
obj_count = prometheus_client.Counter('chronograph_tick_count', 'Total processed object count')


def stop_callback(signum=None, frame=None):
    LOG.info('Received shutdown signal. Stopping main loop...')
    global KEEP_RUNNING
    KEEP_RUNNING = False


async def chronograph_loop():
    LOG.info('Starting chronograph service')
    while KEEP_RUNNING:
        _start_process_time = time()
        REQUEST_ID.set(str(uuid.uuid4()))
        try:
            await asyncio.sleep(1)
            obj_count.inc()
        except Exception as ex:
            raise ex
        finally:
            _end_process_time = time()
            time_tick.observe(_end_process_time - _start_process_time)

if __name__ == '__main__':
    logger.configure_logging()
    loop = asyncio.get_event_loop()
    app_wrapper = metrics.ApplicationWrapper()
    app_wrapper.add_coroutine(chronograph_loop(), stop_callback)
    app_wrapper.run_all()
