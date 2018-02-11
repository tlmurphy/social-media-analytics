# Python Twitter Streams

## Getting Started

### Prerequisites
python 2.7

### Installation

Set up virtualenv (if needed) and install all necessary pip packages:

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install twitter
```

## Usage

Populate the config file with your Twitter consumer key, consumer secret, access key, and access secret.

Then run the program and wait 10 minutes for the result:
```
python stream-sample.py
```

Example output:
```
2018-02-10 18:11:38.101447	2018-02-10 18:21:38.101454
iHeartAwards 	778
BestFanArmy 	584
BTSARMY 	286
EXOL 	259
Sanremo2018 	145
nitiasa 	79
BTS 	64
BestBoyBand 	62
tiposdefic 	60
BestSoloBreakout 	51
```

Don't ask me what BestFanArmy is.
