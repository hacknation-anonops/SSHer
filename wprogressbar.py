#!/usr/bin/python3.4

import time


class ProgressBar:
    def __init__(self, title, maximum):
        self.title = title
        self.maxi = maximum
        self.LENGTH = 50
        self.i = 0

        self.start_time = time.time()
        self.print_bar(0)

    def update(self):
        self.i += 1
        progress = self.LENGTH * self.i // self.maxi if self.maxi else 1
        self.print_bar(progress)

    def print_bar(self, progress):
        percentage = self.i * 100 / self.maxi
        bar = "%s: %.2f %% |%s%s| Time Left: %s" % (
            self.title,
            percentage,
            "\u2588" * progress,
            " " * (self.LENGTH - progress),
            self.time_left()
        )
        if self.i < self.maxi:
            print(bar, end="\r")
        elif self.i == self.maxi:
            print(bar, end="\n")

    def time_left(self):
        duration = time.time() - self.start_time
        eta = duration * self.maxi / self.i if self.i else 0
        time_left = int(eta - duration)
        return self.convert_time(time_left)

    @staticmethod
    def convert_time(number):
        hours = number // 3600
        minutes = (number % 3600) // 60
        seconds = number % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
