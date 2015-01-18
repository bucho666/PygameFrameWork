# -*- coding: utf-8 -*-
import pygame

class Time(object):
    MILLI = 1000.0
    @classmethod
    def now(cls):
        return pygame.time.get_ticks() / cls.MILLI

class Schedule(object):
    _schedules = []
    @classmethod
    def tick(cls):
        now = Time.now()
        for schedule in cls._schedules:
            schedule.execute(now)

    @classmethod
    def add(cls, schedule):
        cls._schedules.append(schedule)

    @classmethod
    def remove(cls, schedule):
        cls._schedules.remove(schedule)

class Job(object):
    def __init__(self, time):
        self._time = Time.now() + time
        Schedule.add(self)

    def execute(self, now):
        if self.is_ready(now): return
        self.job()
        self.done(now)

    def is_ready(self, now):
        return self._time > now

    def done(self, now):
        Schedule.remove(self)

    def job(self):
        pass

class RepeatJob(Job):
    def __init__(self, interval, repeat_max=0):
        Job.__init__(self, interval)
        self._interval = interval
        self._repeat_max = repeat_max
        self._repeat_count = 0

    def done(self, now):
        self._count_up()
        if self._is_done(): Job.done(self, now)
        else: self._repeat(now)

    def _count_up(self):
        if self._repeat_max:
            self._repeat_count += 1

    def _is_done(self):
        return self._repeat_max and\
            self._repeat_count == self._repeat_max

    def _repeat(self, now):
        self._time = now + self._interval

if __name__ == '__main__':
    import sys
    import time
    class WillHello(Job):
        def __init__(self, time):
            Job.__init__(self, time)

        def job(self):
            print 'execute WillHello'

    class WillQuit(Job):
        def __init__(self, time):
            Job.__init__(self, time)

        def job(self):
            sys.exit()

    class CounterJob(RepeatJob):
        def __init__(self, time, number=0):
            RepeatJob.__init__(self, time, number)
            self._count = 0

        def job(self):
            self._count += self._interval
            print self._count

    class Test(object):
        def __init__(self):
            pygame.init()
            WillHello(2)
            WillQuit(3)
            CounterJob(0.1, 3)
            CounterJob(0.5)

        def execute(self):
            while True:
                Schedule.tick()
                time.sleep(0.1) 

    Test().execute()
