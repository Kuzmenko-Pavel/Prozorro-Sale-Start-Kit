import asyncio
import os
import uuid
from datetime import datetime
from time import time

import aiotask_context as context
import prometheus_client

from prozorro_sale import metrics, tools
from prozorro_sale.{{cookiecutter.project_name | to_snake}} import db, utils, errors


LOG = tools.logging.get_custom_logger(__name__)
KEEP_RUNNING = True
# number of seconds to protect procedure from other workers
PROCESSING_LOCK = os.getenv('PROCESSING_LOCK', 1)
time_tick = prometheus_client.Summary('chronograph_tick_latency', 'Time to tick')
timer_diff = prometheus_client.Summary('chronograph_timer_latency', 'Time between procedure.timer and actual date')
obj_count = prometheus_client.Counter('chronograph_tick_count', 'Total processed object count')


def stop_callback(signum=None, frame=None):
    LOG.info('Received shutdown signal. Stopping main loop...')
    global KEEP_RUNNING
    KEEP_RUNNING = False


async def chronograph_loop():
    LOG.info('Starting chronograph service')
    while KEEP_RUNNING:
        _start_process_time = time()
        context.set('X-Request-ID', str(uuid.uuid4()))
        try:
            async with utils.with_notifications(db.read_expired_timer_and_update(PROCESSING_LOCK)) as procedure:
                if not procedure:
                    LOG.debug('No procedures needs to be updated. nooping')
                    await asyncio.sleep(1)
                    continue
                try:
                    timer_diff.observe((datetime.now() - procedure.timer).total_seconds())
                    last_timer_val = procedure.timer
                    procedure._timer_tick()
                    if last_timer_val == procedure.timer:
                        raise Exception(f"procedure.timer hasn't changed after timer tick. proc_id {procedure._id}")
                    obj_count.inc()
                except Exception as ex:
                    raise errors.ChronographTimerException(
                        f'Unexpected error during timer processing {str(ex)}', procedure._id
                    )
                finally:
                    _end_process_time = time()
                    time_tick.observe(_end_process_time - _start_process_time)
        except tools.ConcurrencyError:
            # for now we just do nothing and it will automatically retry in 1 second
            LOG.warning('Failed to update procedure due to concurrency error')
        except errors.ProcedureDeserializationError as ex:
            LOG.exception('Failed to update procedure due to the deserialization error')
            await db.reset_procedure_timer(ex.procedure_id)
        except errors.ChronographTimerException as ex:
            LOG.exception(ex)
            await db.reset_procedure_timer(ex.procedure_id)


def main() -> None:
    tools.check_required_env_vars(
        {'AUCTION_URL', 'AUCTIONS_DATABRIDGE', 'MONGO_URL', 'MONGO_DATABASE', 'NOTIFICATIONS_URL', 'AUTH_URL',
         'REGISTRY_DATABRIDGE'}
    )
    tools.logging.configure_logging()
    loop = asyncio.get_event_loop()
    loop.set_task_factory(context.task_factory)
    app_wrapper = metrics.ApplicationWrapper()
    app_wrapper.add_coroutine(chronograph_loop(), stop_callback)
    app_wrapper.run_all()


if __name__ == '__main__':
    main()
