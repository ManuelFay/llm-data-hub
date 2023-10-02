from typing import Optional


def test_set_conformity(dataset, num_test_samples: Optional[int]) -> int:
    """Make sure the test set is not too big."""
    if num_test_samples:
        return min(num_test_samples, len(dataset) // 2)
    return max(100, len(dataset) // 100)
