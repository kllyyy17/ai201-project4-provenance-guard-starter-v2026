"""Run both signals on four calibration inputs and print them side by side.

    python calibrate.py
"""

import detector
import scoring
import stylometry

SAMPLES = {
    "clearly AI": (
        "Artificial intelligence is transforming the way we live and work. "
        "It offers many benefits for businesses and individuals alike. "
        "Moreover, it improves efficiency and reduces costs in many industries. "
        "Furthermore, it enables better decision making through data analysis. "
        "In conclusion, artificial intelligence plays an important role in modern society."
    ),
    "clearly human": (
        "ok so my landlord finally fixed the heater at 2am, in a thunderstorm, wearing a "
        "raincoat indoors. Nobody tells you that adulthood is mostly negotiating with a guy "
        "named Dmitri about boilers. Anyway. It works now (mostly); I'm still wearing two "
        "sweaters, because trust is earned."
    ),
    "plain human": (
        "I went to the store yesterday. The store was busy, so I waited in line for a while. "
        "Then I bought some milk and bread and went home. My brother was there. We ate dinner "
        "and watched a show."
    ),
    "lightly-edited AI": (
        "Artifcial intelligence is changing how we work, and honestly? Its benefits are huge "
        "for businesses. It improves efficiency and cuts costs in many industries. Data "
        "analysis helps people decide better. Overall AI plays a big role in modern society, "
        "I think."
    ),
}

if __name__ == "__main__":
    print(f"{'input':<20}{'model':>8}{'style':>8}{'combined':>10}")
    for name, text in SAMPLES.items():
        m = detector.model_signal(text)
        s = stylometry.style_signal(text)
        print(f"{name:<20}{m:>8.3f}{s:>8.3f}{scoring.combine_signals(m, s):>10.3f}")
