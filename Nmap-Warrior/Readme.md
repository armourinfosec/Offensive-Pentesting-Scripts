<h1 align="center">Nmap Warrior Python Script</h1>

## Description

This python script automates the process of identifying live hosts from a specified list or a single target. When additional options are provided, the script extends its functionality to include open port scanning, service version detection, and scanning of the most commonly used UDP ports. Designed for cross-platform compatibility, it operates seamlessly on both Linux and Windows systems. This script significantly reduces the manual effort required for these tasks, making it an invaluable resource for security professionals seeking to efficiently collect information about hosts within their scope.


## What makes this script effective?
It approaches four methods to find live hosts:
* Performs ping scan
* Performs TCP SYN ping scan
* Performs TCP ACK ping scan
* Performs UDP ping scan

It provides results in various useful formats:
* xml
* nmap
* gnmap
* Other grabbable formats

## Additional Scanning Features:

* Open port scanning.

* Service version detection.

* Scanning of commonly used UDP ports.

## Installation
To get started, download the script and install the required dependencies:
```
wget https://raw.githubusercontent.com/InfoSecWarrior/Offensive-Pentesting-Scripts/main/Nmap-Warrior/nmap-warrior.py
```
Install the necessary Python packages:
```
pip3 install colorama
```
For Windows only:
```
pip3 install pywin32
```


## Usage

```bash
python3 nmap-warrior.py [-t|--target TARGET] [-l|--list LIST] [Options]
```

### Options:
| Flag | Description |
|------|-------------|
| `-t`, `--target`    | Specify a target domain or IP address. |
| `-l`, `--list`      | Provide a file containing a list of target hosts (one per line). |
| `-o`, `--output`    | Define an output folder (default: `nmap_outputs`). |
| `-s`, `--silent`    | Disable banner display. |
| `-p`, `--portscan`  | Perform an open port scan. |
| `-v`, `--versionscan` | Perform service version detection (requires root privileges). |
| `-u`, `--udpscan`   | Perform UDP port scans with version detection. |


## Examples

1. Scan a single target:
```bash
python3 nmap-warrior.py -t 192.168.1.1
```

2. Scan multiple targets from a file and saving results in a specific directory:
```bash
python3 nmap-warrior.py -l targets.txt -o /path/directory
```


3. Perform a port scan on live hosts:
```bash
python3 nmap-warrior.py -t 192.168.1.1 -p
```

4. Perform version detection:
```bash
python3 nmap-warrior.py -t 192.168.1.1 -p -v
```

5. Perform a UDP scan:
```bash
python3 nmap-warrior.py -t 192.168.1.1 -u
```

## Prerequisites

- **Python 3**
- **Nmap**
- **Notify** (optional).
