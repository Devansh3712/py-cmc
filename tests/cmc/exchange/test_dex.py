import random
import time
from cmc import Dex


def test_get_data() -> None:
    result = Dex().get_data
    time.sleep(2)
    index = random.randint(1, len(result))
    assert len(result[index]) == 5