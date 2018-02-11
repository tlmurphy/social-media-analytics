# Landslide.py

Outputs top 10 videos in the past 24 hours based on the keyword 'landslide.'

## Getting Started

### Prerequisites
python 2.7

### Installation

Set up virtualenv (if needed) and install all necessary pip packages:

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install google-api-python-client
pip install rfc3339
```

## Usage

You'll need to set an environment variable for the Youtube API Developer Key:
```bash
export YT_DEV_KEY=yourdevkey
```

Example output:
```
python landslide.py

2018-01-26T16:27:37-06:00	2018-01-27T16:27:37-06:00

lVfG-dP0JaA	Miley Cyrus Performing Landslide at MusiCares 2018 HD	13392
Lt7bhAWW9TY	Miley Cyrus - Landslide (Live at MusiCares Fleetwood Mac Tribute)	7552
H72F7fK5doI	Miley Cyrus singing Fleetwood Mac’s Landslide 2018 MusiCares Person of the Year	751
bOOWcAp5JMw	Miley Cyrus - Landslide (Cover - Lyrics)	514
qfGmCb9iXq0	Miley Cyrus - Landslide	416
EGUvArAKkvY	Miley Cyrus - Landslide - MusiCares Person of the Year - 26/1/ 2018	98
Ow6QdelaJC8	Trixie Mattel - Sk8er Boi/Landslide Medley (Now With Moving Parts - Live in London, 25/01/18)	57
r1PxC_eQH8E	Miley Cyrus - Landslide (Live at the MusiCares 2018) "Person of the Year"	41
CNBjx9MZHH0	Stevie Nicks Offers Up a LANDSLIDE of Thoughts and Thanks at Close of 24 Karat Gold Tour	35
H49FmYmutxA	SCI03 - DRRR - MAPUA - G106 - EARTHQUAKE INDUCED LANDSLIDE	28
```
