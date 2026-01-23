"""
Runtime metrics collection for Vision I (polished).
"""

import time
from collections import Counter, deque


class MetricsCollector:
    def __init__(self, window_seconds=60):
        self.start_time = time.time()
        self.window_seconds = window_seconds

        self.alert_times = deque()
        self.object_counter = Counter()

    def record(self, label):
        """
        Record a new alert event.
        """
        now = time.time()
        self.alert_times.append(now)

        if label:
            self.object_counter[label] += 1

        self._trim_old_events()

    def _trim_old_events(self):
        """
        Remove events outside the rolling window.
        """
        cutoff = time.time() - self.window_seconds
        while self.alert_times and self.alert_times[0] < cutoff:
            self.alert_times.popleft()

    def alerts_per_minute(self):
        if not self.alert_times:
            return 0.0
        return len(self.alert_times) * (60 / self.window_seconds)

    def average_response_time(self):
        if len(self.alert_times) < 2:
            return 0.0

        intervals = [
            self.alert_times[i] - self.alert_times[i - 1]
            for i in range(1, len(self.alert_times))
        ]
        return sum(intervals) / len(intervals)

    def most_common_object(self):
        if not self.object_counter:
            return None
        return self.object_counter.most_common(1)[0]
