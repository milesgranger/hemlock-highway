import logging
import redis
import time
import sys

if __name__ == '__main__':
    time.sleep(4)  # Wait for redis container to be started

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    attempts = 3
    for attempt in range(attempts):

        try:
            logger.info('Compute container connecting to Redis..')
            con = redis.StrictRedis(host='redis-service', port=6379, decode_responses=True)
            logger.info('Compute container successfully connected and running!')

            while True:
                records = con.keys()
                if records:
                    logger.info('Compute container got records: {}...processing request(s)'.format(records))

                    for job in records:
                        logger.info('Processing job: {}'.format(job))
                        # TODO: Logic to process acquired jobs.
                        time.sleep(2)
                        logger.info('Finished job: {} - Removing from Redis Job Queue...'.format(job))
                        result = con.delete(job)
                        logger.info('Removed job {} from Redis with code: {}'.format(job, result))
                else:
                    time.sleep(5)

        except Exception as exc:
            logger.exception('')
            logger.critical('Experience error {} out of {} allowed attempts.'.format(attempt+1, attempts))
    logger.error('Tried to resolve error {} times, container exiting...'.format(attempts))
    sys.exit(1)





