import random
import time
from cmc import RecentlyAdded


def test_get_data() -> None:
    result = RecentlyAdded().get_data
    time.sleep(2)
    index = random.randint(0, len(result))
    assert len(result) == 30
    assert len(result[index]) == 12