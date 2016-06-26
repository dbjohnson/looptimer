# looptimer
Progress bar style loop timer with projected time-to-completion.

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
