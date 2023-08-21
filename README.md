# Tusur API
![PyPI](https://img.shields.io/pypi/v/tusur?color=orange) ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Weebp-Team/tusur?color=blueviolet) ![License](https://img.shields.io/pypi/l/tusur?color=blueviolet) ![Forks](https://img.shields.io/github/forks/Weebp-team/tusur?style=social)

Python library for working with site TUSUR

## Installation

```sh
pip install tusur 
```

## Usage
How get timetable by group:
```python
from tusur import Timetable

>>> timetable = Timetable()
>>> timetable.get_timetable("571-2", week_id=666)
>>> [
    {
    "day": "Mon, May 22",
    "lessons": [
        {
            "time": "08:50 10:25",
            "discipline": null,
            "view": null,
            "teacher": null
        },
        {
            "time": "10:40 12:15",
            "discipline": null,
            "view": null,
            "teacher": null
        },
    ...
    ]
    }
    ]
```


## Dependencies

- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Contributing

Bug reports and/or pull requests are welcome

## License

[MIT](https://choosealicense.com/licenses/mit/)