# Knitting Pattern to Chart Translator
This is a program to help create knitting charts from knitting patterns.

Currently, the application only allows for input of typed, structured knitting patterns for items knitted flat and outputs ASCII charts.

# Getting Started
## Prerequisites
You'll need:
- Python 3.10.7 or later

## Installation
1. Navigate to the root folder of the project
2. Download the requirements using `pip install -r requirements.txt`
3. Run `python3 setup.py install` to install the CLI app
4. The CLI app can now be run with `pattern_to_chart start`

## Using the App
When the app is started, you can follow the prompts to be able to enter your pattern.

NOTE:
- Stitches are entered using their abbreviations as a comma separated list like: k2, p2, k, p

- Repeats can be entered using the following formats:
    - "\*k2, p2\*; repeat from \* to \* 5 times" OR "(k2, p2) x 5" OR "\*k2, p2\*"

Currently, only the following stitches are supported:
- Knit (k)
- Purl (p)
- Yarn Over (yo)
- Knit in Front and Back (kfb)
- Knit 2 Together (k2tog)
- Purl 2 Together (p2tog)
- Slip Slip Knit (ssk)
- Slip Slip Purl (ssp)
- Slip 2, Knit 1, Pass 2 Slipped Stitches Over (s2kp2)