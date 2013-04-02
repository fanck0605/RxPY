from datetime import datetime, timedelta
from time import sleep
from rx.concurrency import TimeoutScheduler

def test_timeout_now():
    res = TimeoutScheduler.now() - datetime.utcnow()
    assert res < timedelta(microseconds=1000)


def test_timeout_schedule_action():
    scheduler = TimeoutScheduler()
    ran = False
    
    def action(scheduler, state):
        print ("action()")
        nonlocal ran
        ran = True

    scheduler.schedule(action)

    sleep(0.1)
    assert (ran == True)

def test_thread_pool_schedule_action_due():
    scheduler = TimeoutScheduler()
    starttime = datetime.utcnow()
    endtime = None
    
    def action(scheduler, state):
        nonlocal endtime
        endtime = datetime.utcnow()
    
    scheduler.schedule_relative(timedelta(milliseconds=200), action)

    sleep(0.3)
    diff = endtime-starttime
    assert(diff > timedelta(milliseconds=180))
    
def test_timeout_schedule_action_cancel():
    ran = False
    scheduler = TimeoutScheduler()

    def action(scheduler, state):
        ran = True
    d = scheduler.schedule_relative(timedelta(milliseconds=1), action)
    d.dispose()

    sleep(0.1)
    assert (not ran)