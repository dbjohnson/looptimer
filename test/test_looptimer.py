import unittest
import contextlib
import sys
import time
from StringIO import StringIO

from looptimer import timedloop


@contextlib.contextmanager
def capture():
    captured = {}
    try:
        stdout_orig = sys.stdout
        captured = StringIO()
        sys.stdout = captured
        yield captured
    finally:
        sys.stdout = stdout_orig


class TestLoopTimer(unittest.TestCase):
    def test_looptimer(self):
        expected = [u'|xx                  | 1 / 10 (10%) loops completed in 0 seconds; ~1 second remaining',
                    u'|xxxx                | 2 / 10 (20%) loops completed in 0 seconds; ~1 second remaining',
                    u'|xxxxxx              | 3 / 10 (30%) loops completed in 0 seconds; ~1 second remaining',
                    u'|xxxxxxxx            | 4 / 10 (40%) loops completed in 0 seconds; ~1 second remaining',
                    u'|xxxxxxxxxx          | 5 / 10 (50%) loops completed in 1 second; ~1 second remaining',
                    u'|xxxxxxxxxxxx        | 6 / 10 (60%) loops completed in 1 second; ~0 seconds remaining',
                    u'|xxxxxxxxxxxxxx      | 7 / 10 (70%) loops completed in 1 second; ~0 seconds remaining',
                    u'|xxxxxxxxxxxxxxxx    | 8 / 10 (80%) loops completed in 1 second; ~0 seconds remaining',
                    u'|xxxxxxxxxxxxxxxxxx  | 9 / 10 (90%) loops completed in 1 second; ~0 seconds remaining',
                    u'|xxxxxxxxxxxxxxxxxxxx| 10 / 10 (100%) loops completed in 2 seconds',
                    u'']

        with capture() as c:
            for _ in timedloop(xrange(10), bar_char='x', animate=False):
                time.sleep(0.2)
        captured = c.getvalue().split('\n')

        self.assertListEqual(expected, captured)
