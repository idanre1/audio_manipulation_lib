import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from retempo import bpm_from_beats


def test_bpm_uses_median_interval():
    assert bpm_from_beats([0.0, 0.5, 1.0, 1.7, 2.2]) == pytest.approx(120)


def test_bpm_needs_two_beats():
    with pytest.raises(ValueError):
        bpm_from_beats([1.0])
