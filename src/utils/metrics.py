"""
Runtime metrics collection for Vision I.
"""

import time
from collections import Counter


class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.alert_times = []
        self.object_counter = Counter()

    def record(self, label):
        """
        Record a new alert event.
        """
        now = time.time()
        self.alert_times.append(now)

        if label:
            self.object_counter[label] += 1

    def alerts_per_minute(self):
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return 0
        return len(self.alert_times) / (elapsed / 60)

    def average_response_time(self):
        if len(self.alert_times) < 2:
            return 0

        intervals = [
            self.alert_times[i] - self.alert_times[i - 1]
            for i in range(1, len(self.alert_times))
        ]
        return sum(intervals) / len(intervals)

    def most_common_object(self):
        if not self.object_counter:
            return None
        return self.object_counter.most_common(1)[0]
