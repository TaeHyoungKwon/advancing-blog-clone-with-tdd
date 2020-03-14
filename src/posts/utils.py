import datetime
import re

from django.utils.html import strip_tags


def get_read_time(html_string):
    def _count_words():
        matching_words = re.findall(r"\w+", strip_tags(html_string))
        return len(matching_words)

    read_time_min = _count_words() / 200.0  # assuming 200wpm reading
    read_time = str(datetime.timedelta(seconds=read_time_min))
    return int(read_time_min)
