# WMX R2 Documentation

**WMX R2™ — The Real-Time Execution Layer for Physical AI**

Technical documentation for **WMX R2**, a complete real-time robotics solution for Physical AI that integrate a ROS 2 interface with the [MOVENSYS](https://www.movensys.com/) WMX3 motion engine it runs on. ("R2" stands for *Real-time Robotics*.)

> ROS is a trademark of Open Robotics.

**Documentation Site:** https://movensys.github.io/wmx-r2-doc/

## Overview

WMX R2 combines a ROS 2 interface with the MOVENSYS WMX3 EtherCAT-based motion engine in a single solution, enabling control of robotic manipulators (e.g., Dobot CR3A) with motion planning through MoveIt2 and NVIDIA Isaac cuMotion.

## Documentation Contents

| Section | Description |
|---------|-------------|
| **Getting Started** | System requirements, ROS2 installation, workspace setup, mock & physical hardware, architecture |
| **Packages** | `wmx_r2_message` and `wmx_r2_package` node documentation |
| **Integration** | MoveIt2, NVIDIA Isaac cuMotion, custom planner & application guides |
| **API Reference** | ROS2 services, topics, and actions |
| **Demo application** | NVIDIA Jetson Orin and Intel x86_64 setups |
| **Deployment** | Source build, Debian package, and Docker options |
| **Troubleshooting** | Common issues and solutions |

## Building Locally

### Prerequisites

- Python 3.10+

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r doc/requirements.txt
```

### Build

```bash
cd doc
make clean
make html
```

Open `doc/_build/html/index.html` in your browser to view the documentation.

## Deployment

Documentation is automatically built and deployed to GitHub Pages via GitHub Actions on every push to `main`.


## License

Copyright 2026 MOVENSYS. All rights reserved. 

