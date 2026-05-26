# MLB Pitch Arsenal Analyzer

This project analyzes Paul Skenes' 2025 pitch arsenal using Statcast data from `pybaseball`. The notebook pulls pitcher-level pitch data, cleans the core columns, summarizes pitch usage, and creates charts for velocity, whiff rate, and strike rate.

## Scouting Summary

Paul Skenes' arsenal is built around premium velocity and a deep mix of secondary pitches. Across 3,207 tracked pitches from March 11, 2025 through September 24, 2025, his four-seam fastball was the foundation of the profile, accounting for 39.5% of pitches at an average velocity of 98.2 mph. He also featured a hard sinker at 97.6 mph and a split-finger at 93.7 mph, giving him multiple power offerings that can attack different parts of the zone.

The strongest swing-and-miss result came from the changeup, which produced a 22.0% whiff rate despite being used only 10.8% of the time. The slider and sweeper also generated above-average miss rates, giving Skenes several ways to finish at-bats beyond simply overpowering hitters with fastball velocity.

From a command perspective, the four-seam fastball and sinker were the most reliable strike-getters, with strike rates of 69.8% and 67.3%. That combination gives Skenes a strong base for getting ahead in counts, while his changeup, sweeper, slider, and split-finger provide different shapes for chase and weak contact.

## Pitch Mix

| Pitch | Usage Rate | Avg Velocity | Whiff Rate | Strike Rate |
|---|---:|---:|---:|---:|
| 4-Seam Fastball | 39.5% | 98.2 mph | 13.8% | 69.8% |
| Sweeper | 15.7% | 84.5 mph | 14.3% | 63.3% |
| Split-Finger | 14.2% | 93.7 mph | 11.0% | 62.4% |
| Changeup | 10.8% | 88.7 mph | 22.0% | 54.6% |
| Sinker | 10.0% | 97.6 mph | 7.2% | 67.3% |
| Slider | 5.4% | 85.3 mph | 15.7% | 65.1% |
| Curveball | 4.5% | 83.9 mph | 13.8% | 53.1% |

## Charts

![Paul Skenes Average Velocity by Pitch](outputs/skenes_velocity.png)

![Paul Skenes Whiff Rate by Pitch](outputs/skenes_whiff_rate.png)

![Paul Skenes Strike Rate by Pitch](outputs/skenes_strike_rate.png)


## Tools Used

- Python
- pandas
- matplotlib
- pybaseball
- Jupyter Notebook
