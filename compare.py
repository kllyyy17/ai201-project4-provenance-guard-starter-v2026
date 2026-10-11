"""Print both signals for each piece of text given as an argument.

    python compare.py "first piece" "second piece" "third piece"
"""

import sys

import detector
import stylometry

if __name__ == "__main__":
    print(f"{'piece':<34}{'model':>8}{'style':>8}{'gap':>8}")
    for text in sys.argv[1:]:
        m = detector.model_signal(text)
        s = stylometry.style_signal(text)
        print(f"{text[:31] + '...':<34}{m:>8.3f}{s:>8.3f}{abs(m - s):>8.3f}")
