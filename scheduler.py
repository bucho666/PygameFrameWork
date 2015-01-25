# -*- coding: utf-8 -*-
import pygame

class Scheduler(object):
    _schedules = []
    @classmethod
    def tick(cls):
        for schedule in list(cls._schedules):
            cls._execute_schedule(schedule)

    @classmethod
    def _execute_schedule(cls, schedule):
        if schedule.is_running():
            schedule.execute()
            return
        schedule.execute_last_action()
        cls._schedules.remove(schedule)

    @classmethod
    def add(cls, schedule):
        cls._schedules.append(schedule)

class Schedule(object):
    def __init__(self, frame):
        self._frame = frame
        self._action = self.NullAction()
        self._last_action = self.NullAction()
        Scheduler.add(self)

    def last(self, action):
        self._last_action = action
        return self

    def action(self, action):
        self._action = action
        return self

    def execute(self):
        self._action()
        self._frame -= 1

    def execute_last_action(self):
        self._last_action()

    def is_running(self):
        return self._frame > 0

    class NullAction(object):
        def __call__(self):
            pass

class Job(object):
    def __init__(self, wait_frame):
        self._wait_frame = wait_frame
        Schedule.add(self)

    def execute(self):
        if self.is_ready(): return
        self.action()
        self.done()

    def is_ready(self):
        self._wait_frame -= 1
        return self._wait_frame > 0

    def done(self):
        Schedule.remove(self)

    def action(self):
        pass

class RepeatJob(Job):
    def __init__(self, interval, repeat_max=0):
        Job.__init__(self, interval)
        self._interval = interval
        self._repeat_max = repeat_max
        self._repeat_count = 0

    def done(self):
        self._count_up()
        if self._is_done(): Job.done(self)
        else: self._repeat()

    def _count_up(self):
        if self._repeat_max:
            self._repeat_count += 1

    def _is_done(self):
        return self._repeat_max and\
            self._repeat_count == self._repeat_max

    def _repeat(self):
        self._wait_frame = + self._interval

if __name__ == '__main__':
    import sys
    import time

    class TestJob(object):
        def first(self):
            print 'first'
            return self

        def action(self):
            print 'action'

        def last(self):
            print 'last'
            sys.exit(0)

    class Test(object):
        def __init__(self):
            pygame.init()
            j = TestJob().first()
            Schedule(4).action(j.action).last(j.last)

        def execute(self):
            while True:
                Scheduler.tick()
                time.sleep(0.1) 

    Test().execute()
