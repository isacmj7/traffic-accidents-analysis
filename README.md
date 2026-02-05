# Traffic Accidents Analysis (India)

**Ishak Islam** | UMID28072552431 | Unified Mentor Internship

## About

Analysis of road traffic accidents in India using official government data from the Ministry of Road Transport and Highways (MoRTH). The dataset covers state-wise statistics, collision types, traffic violations, safety device usage, and fatality patterns from 2019-2023.

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_traffic_accidents_analysis.ipynb
```

Run all cells to see the analysis.

## Dataset

Download from: https://data.opencity.in/dataset/road-accidents-in-india-2023

Required CSV files to place in `data/` folder:
- `state_wise_accidents.csv` - State-wise road accidents (2019-2023)
- `state_wise_fatalities.csv` - State-wise fatalities (2019-2023)
- `collision_types.csv` - Accidents by collision type
- `violations.csv` - Accidents by violation type
- `safety_devices.csv` - Accidents with absent safety devices
- `road_users_fatalities.csv` - Fatalities by road user type

## Files

```
├── data/           # Put dataset files here
├── notebooks/      # Analysis notebook
├── scripts/        # Helper functions
├── visualizations/ # Charts
├── tableau/        # Tableau exports
└── docs/           # Documentation
```

## Results

- State-wise accident analysis with 5-year trends
- Identification of top accident-prone states
- Analysis of collision types and traffic violations
- Safety device compliance patterns
- Fatality patterns by road user type
- Data exports ready for Tableau dashboards

## Tableau Dashboard

**Live Interactive Dashboard:** [View on Tableau Public](https://public.tableau.com/app/profile/ishak.islam/viz/TrafficAccidentsAnalysisIndia/Dashboard?publish=yes)

## Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn, Tableau

## GitHub Repository

**Source Code:** [https://github.com/isacmj7/traffic-accidents-analysis](https://github.com/isacmj7/traffic-accidents-analysis)
