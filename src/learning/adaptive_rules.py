"""
Adaptive threshold logic for Vision I.

Adjusts decision thresholds dynamically based on
observed alert frequency.
"""


class AdaptiveThresholds:
    def __init__(
        self,
        base_center_distance=1.5,
        base_side_distance=2.0,
        min_distance=1.0,
        max_distance=3.0
    ):
        self.center_distance = base_center_distance
        self.side_distance = base_side_distance

        self.min_distance = min_distance
        self.max_distance = max_distance

        self.center_alert_count = 0
        self.side_alert_count = 0

    def update(self, decision: str):
        """
        Update alert counters based on the decision.
        """
        if not decision:
            return

        if "ahead" in decision.lower():
            self.center_alert_count += 1

        if "left" in decision.lower() or "right" in decision.lower():
            self.side_alert_count += 1

        self._adapt_thresholds()

    def _adapt_thresholds(self):
        """
        Adjust thresholds based on alert frequency.
        """
        # If center alerts are too frequent, loosen threshold
        if self.center_alert_count > 5:
            self.center_distance = min(
                self.center_distance + 0.1,
                self.max_distance
            )
            self.center_alert_count = 0

        # If side alerts are too frequent, loosen threshold
        if self.side_alert_count > 5:
            self.side_distance = min(
                self.side_distance + 0.1,
                self.max_distance
            )
            self.side_alert_count = 0

    def get_center_threshold(self):
        return self.center_distance

    def get_side_threshold(self):
        return self.side_distance
