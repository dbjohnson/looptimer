# -*- coding: utf-8 -*-
import sys
import time


DEFAULT_BAR_WIDTH = 20
DEFAULT_BAR_CHAR = u'█'


class LoopTimer:
    """
    Loop iteration timer.  Measures iteration progress and provides estimated
    time to completion by calculating average loop pass execution time and
    projecting that average over the number of passes remaining

    Args:
        total_iterations (int): number of loop iterations

    Keyword Args:
        label (str, default None): descriptive label, printed to the left of the progress bar
        bar_char (str, default u'█'): character used to fill in the progress bar
        bar_width (int, default 20): progress bar width in characters
        animate (bool, default True): disable to print each update on a new line (useful when interspersed with other log messages)

    Usage:
    t = LoopTimer(...)
    for i in iterable:
        ...
        t.tick()

    """
    def __init__(self, total_iterations, label=None,
                 bar_char=DEFAULT_BAR_CHAR,
                 bar_width=DEFAULT_BAR_WIDTH,
                 animate=True):
        self.total_iterations = total_iterations
        self.iterations_elapsed = 0
        self.label = label
        self.start_time = self.last_update_time = time.time()
        self.last_printed_width = 0
        self.bar_char = bar_char
        self.bar_width = bar_width
        self.animate = animate

    def tick(self):
        self.iterations_elapsed += 1
        self.__print_status()

    def pct_complete(self):
        return (100. * self.iterations_elapsed) / self.total_iterations

    def __print_status(self):
        secs_elapsed = time.time() - self.start_time
        pct_complete = self.pct_complete()
        completed_bar_width = int(pct_complete * self.bar_width / 100)
        tgo_bar_width = self.bar_width - completed_bar_width
        bar = u'|' + (self.bar_char * completed_bar_width) + (u' ' * tgo_bar_width) + u'|'
        elapsed = _seconds_to_time_string(secs_elapsed)
        tgo = _seconds_to_time_string(self.seconds_remaining())
        status = u'{label}{bar} {completed} / {total} ({pct:.0f}%) loops completed in {elapsed}{tgo}'.format(
            label='{}: '.format(self.label) if self.label else '',
            pct=pct_complete,
            bar=bar,
            completed=self.iterations_elapsed,
            total=self.total_iterations,
            elapsed=elapsed,
            tgo='; ~{} remaining'.format(tgo) if pct_complete < 100 else '')

        if self.animate:
            # back up to beginning of line and make sure to overwrite the previous message
            padding = self.last_printed_width - len(status)
            if padding > 0:
                status += u' ' * padding

            self.last_printed_width = len(status)
            sys.stdout.write(u'\r{}'.format(status))
            if pct_complete >= 100:
                sys.stdout.write('\n')
        else:
            sys.stdout.write(u'{}\n'.format(status))

        sys.stdout.flush()

    def __seconds_per_iteration(self):
        return (time.time() - self.start_time) / self.iterations_elapsed

    def seconds_remaining(self):
        return self.__seconds_per_iteration() * (self.total_iterations - self.iterations_elapsed)


def timedloop(iterable, label=None,
              bar_char=DEFAULT_BAR_CHAR,
              bar_width=DEFAULT_BAR_WIDTH,
              animate=True):
    """
    Iteration timer - directly wraps any iterable.
    Measures iteration progress and provides estimated time to completion by
    calculating average loop pass execution time and projecting that average
    over the number of passes remaining

    Args:
        iterable (iterable): iterable sequence

    Keyword Args:
        label (str, default None): descriptive label, printed to the left of the progress bar
        bar_char (str, default u'█'): character used to fill in the progress bar
        bar_width (int, default 20): progress bar width in characters
        animate (bool, default True): disable to print each update on a new line (useful when interspersed with other log messages)

    """
    t = LoopTimer(len(iterable), label=label, bar_char=bar_char, bar_width=bar_width, animate=animate)
    for i in iterable:
        yield
        t.tick()


def _seconds_to_time_string(seconds):
    hours, seconds = divmod(int(seconds), 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d} hours'.format(hours, minutes, seconds)
    elif minutes > 0:
        return '{:d}:{:02d} minutes'.format(minutes, seconds)
    elif seconds == 1:
        return '1 second'
    else:
        return '{:d} seconds'.format(seconds)
