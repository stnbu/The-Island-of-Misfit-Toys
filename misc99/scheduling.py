import time
import datetime

class WeekTime(object):

    def __init__(self, struct_time):
        self.struct_time = self._normalize(struct_time)

    def _normalize(self, struct_time):
        # tm_year=0, tm_mon=0, tm_mday=0, tm_hour=4, tm_min=4, tm_sec=5, tm_wday=2, tm_yday=0, tm_isdst=-1
        t = time.struct_time((
            0,  # tm_year
            0,  # tm_mon
            0,  # tm_mday
            struct_time.tm_hour,
            struct_time.tm_min,
            struct_time.tm_sec,
            struct_time.tm_wday,
            0,  # tm_yday
            -1,  # tm_isdst
        ))
        return t

    def __gt__(self, value):
        return self.struct_time > value.struct_time

    def __lt__(self, value):
        return self.struct_time < value.struct_time

    def __ge__(self, value):
        return self.struct_time >= value.struct_time

    def __le__(self, value):
        return self.struct_time <= value.struct_time

    def __eq__(self, value):
        return self.struct_time == value.struct_time

class Schedule(object):

    def __init__(self, windows):
        self.windows = windows

    def __contains__(self, weektime):
        for window in self.windows:
            start, end = window
            if weektime >= start and weektime <= end:
                return True
        return False

if __name__ == '__main__':
    start = WeekTime(time.struct_time((0,0,0,4,0,0,2,0,-1)))
    end = WeekTime(time.struct_time  ((0,0,0,9,0,0,2,0,-1)))

    schedule = Schedule([(start, end)])

    proposed = WeekTime(time.struct_time((0,0,0,5,0,0,2,0,-1)))
    print proposed in schedule
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    proposed = WeekTime(time.struct_time((0,0,0,5,0,0,5,0,-1)))
    print proposed in schedule
