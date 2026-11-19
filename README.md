# 2D Vehicle Simulation

## How to run the code
Installing the dependencies
```bash
python3 -m venv .venv
pip install -r ./requirements.txt
```

Running the code
```bash
python main.py
```

## Project Structure
```bash
.
├── mplstyles/ # some custom style I use sometimes
├── tracks/ # track in csv formats
│   ├── edgecase_waypoints.csv
│   └── silverstone_waypoints.csv
├── main.py # entry point
├── controller.py # control how the car steers and accelerate
├── track.py # load or generate the track
├── vehicle.py # vehicle data
├── requirements.txt
└── README.md
```
