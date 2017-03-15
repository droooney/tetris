from threading import Timer as ThreadTimer
from time import time


class Timer:
    def __init__(self, interval, function, args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or {}

        self._is_ended = False
        self._timer = None
        self._to_call = lambda: function(*args, **kwargs)
        self._time = time()
        self._time_left = interval

        self.resume()

    def _on_end(self):
        self._is_ended = True
        self._to_call()

    def cancel(self):
        if self._is_ended:
            return self

        self._timer.cancel()
        self._is_ended = True

        return self

    def resume(self):
        if self._is_ended:
            return self

        self._timer = ThreadTimer(self._time_left, self._on_end)
        self._timer.start()

        return self

    def pause(self):
        if self._is_ended:
            return self

        self._timer.cancel()

        new_time = time()
        self._time_left = self._time_left - new_time + self._time
        self._time = new_time

        return self
