# looptimer

Progress bar style loop timer with projected time-to-completion.

[![Code Climate](https://codeclimate.com/github/dbjohnson/looptimer/badges/gpa.svg)](https://codeclimate.com/github/dbjohnson/looptimer)
[![License](https://img.shields.io/github/license/dbjohnson/looptimer.svg)]()
[![PyPi](https://img.shields.io/pypi/v/looptimer.svg)](https://pypi.python.org/pypi/looptimer)

## Installation
```pip install looptimer```

## Usage
```python
from looptimer import timedloop

for _ in timedloop(range(100), label='foo'):
	...
```

### Sample output
![](demo.png)
