import threading
import time
import datetime
import os
import sys

import cream_testsuite_conf
import cream_testing

class SubmissionThread(threading.Thread):
    '''
       This class is used to submit n jobs 
       Its use is mainly to monitor memory usage during submission 
       process.
    '''
    def __init__(self, msg_queue, job_num, jdl_fname):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.working = None
        self.msg_queue = msg_queue
        self.cream_job_ids = list()
        self.job_num = job_num
        self.jdl_fname = jdl_fname

        try:
            self.my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
        except Exception:
            self.msg_queue.put(sys.exc_info())

    def run(self):

        self.working = True
        print "Submitting %s jobs" % self.job_num
        for i in range(self.job_num):
            try:
                ce = ce_endpoint = self.my_conf.getParam('submission_info', 'ce_endpoint') + "/" + self.my_conf.getParam('submission_info', 'cream_queue')
                cream_job_id = cream_testing.submit_job(self.jdl_fname, ce)
                self.cream_job_ids.append(cream_job_id)
            except Exception:
                self.msg_queue.put(sys.exc_info())
            time.sleep(2)

        print "%s jobs submitted" % self.job_num
        self.working = False

    def stop(self):
        self._stop.set()

    def is_stopped(self):
        return self._stop.isSet()

    def still_working(self):
        return self.working



