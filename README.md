# Knitting Pattern to Chart Translator
This is a program to help create knitting charts from knitting patterns.

Currently, the application only allows for input of typed, structured knitting patterns for items knitted flat and outputs ASCII charts.

# Getting Started
## Prerequisites
You'll need:
- Python 3.10.7 or later

## Installation
1. Navigate to the root folder of the project
2. Run `python3 setup.py install`
3. The CLI app can now be run with `pattern_to_chart parse "enter pattern here"`

## Using the App
Stitches are entered using their abbreviations as a comma separated string like:
`pattern_to_chart parse "k2, p2, k2"`

Multiple lines can be entered by just not closing the quotation marks like:
```
pattern_to_chart parse "cast on 10 sts
row 1: k10
row 2: k3, p4, k3"
```

Repeats can be entered using the following formats:
```
pattern_to_chart parse "row 1: k1, *k2, p2*; repeat from * to * 5 times, k1"
```
OR
```
pattern_to_chart parse "cast on 12 stitches,
row 1: k, *k2, p2*, k"
```
If the latter is used, the number of cast on stitches must be stated.

Currently, only the following stitches are supported:
- Knit (k)
- Purl (p)
- Yarn Over (yo)
- Knit 2 Together (k2tog)
- Slip Slip Knit (ssk)