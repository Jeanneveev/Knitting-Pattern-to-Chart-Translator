"""The current dictionary of stitch abbreviations and their names and symbols"""

STITCH_BY_ABBREV = {
    "k":    {"type": "reg",  "stitches_consumed": 1, "stitches_produced": 1, "rs": " ",   "ws": "-",   "name": "knit"},
    "p":    {"type": "reg",  "stitches_consumed": 1, "stitches_produced": 1, "rs": "-",   "ws": " ",   "name": "purl"},
    "yo":   {"type": "incr", "stitches_consumed": 0, "stitches_produced": 1, "rs": "O",   "ws": "O",   "name": "yarn over"},
    "kfb":  {"type": "incr", "stitches_consumed": 1, "stitches_produced": 2, "rs": "Y",   "ws": "Y",   "name": "knit in front and back"},
    "k2tog":{"type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "/",   "ws": "/.",  "name": "knit 2 together"},
    "p2tog":{"type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "/.",  "ws": "/",   "name": "purl 2 together"},
    "ssk":  {"type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "\\",  "ws": "\\.", "name": "slip slip knit"},
    "ssp":  {"type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "\\.", "ws": "\\",  "name": "slip slip purl"},
    "s2kp2":{"type": "decr", "stitches_consumed": 3, "stitches_produced": 1, "rs": "^",   "ws": "^",   "name": "slip 2, knit 1, pass 2 slipped stitches over"}
}