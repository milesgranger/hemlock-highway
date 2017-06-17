import os
import logging
import redis
import time
import sys

from ast import literal_eval

from linear_regression.model import ModelRunner as RegressionModelRunner

class ComputeServiceHandler:

    def __init__(self):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self.logger.addHandler(streamHandler)

    def run(self):
        """
        Process jobs if in debug mode (this container never stops)
        Otherwise process the one job if in production, since this will be running as a single container
        with one job-id to process.
        """
        if os.environ.get('DEBUG', False):
            self.process_jobs_debug_mode()
        else:
            self.process_job()

    def submit_job_to_model(self, job):
        """
        Based on job (json) architecture, submit it to the appropriate model's main runner.
        """


    def process_jobs_debug_mode(self):
        """Process job while running on a local container"""
        attempts = 3
        for attempt in range(attempts):

            try:
                self.logger.info('Compute container connecting to Redis..')
                con = redis.StrictRedis(host='redis-service', port=6379)
                self.logger.info('Compute container successfully connected and running!')

                while True:
                    records = con.keys()
                    if records:
                        self.logger.info('Compute container got records: {}...processing request(s)'.format(records))

                        for job_id in records:
                            self.logger.info('Processing job: {}'.format(job_id))
                            # TODO: Logic to process acquired jobs.
                            job = con.get(job_id).decode()
                            job = literal_eval(job)
                            self.logger.info('Job details: {}'.format(job))

                            if job.get('model-type') == 'regression':
                                RegressionModelRunner(model_architecture=job, logger=self.logger)

                            self.logger.info('Finished job: {} - Removing from Redis Job Queue...'.format(job))
                            result = con.delete(job_id)
                            self.logger.info('Removed job {} from Redis with code: {}'.format(job, result))
                    else:
                        time.sleep(5)

            except Exception as exc:
                self.logger.exception('')
                self.logger.critical('Experience error {} out of {} allowed attempts.'.format(attempt + 1, attempts))
        self.logger.error('Tried to resolve error {} times, container exiting...'.format(attempts))
        sys.exit(1)


    def process_job(self):
        """Process job while running on AWS Batch"""
        raise NotImplementedError('Not yet running on AWS Batch')

if __name__ == '__main__':
    time.sleep(4)  # Wait for redis container to be started
    handler = ComputeServiceHandler()
    handler.run()




