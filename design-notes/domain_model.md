A knitting *pattern* is identified by its *name* and its *creator's name*.
A pattern can be made up of one or more *sections*. A *section* is identified by its name like "Sleeve", "Back", "Section 1", or "Section with Increases". A section has its own *pattern*, which is used to make a part of the whole pattern.
For more detailed patterns, a section might also be split into *parts*, which is like a sub-section. It also has a *name* and a *pattern*.

A pattern, in any sense, is a set of instructions on which stitches to knit in what order. A pattern is split up into *rows*, which is identified by its *row number* and contains a list of *stitches*. A row may also have a note on whether the row is on the *right* or *wrong side* and/or whether it is a *increase* or *decrease row* and/or whether it is a *cast-on row* or *set-up row*. The *cast-on row* is technically not a row, it's the adding of the initial number of stitches for the pattern. While a normal row in a pattern might look like:
"Row 3: k1, p2, k1"
a cast on looks like:
"Cast on 96 sts"

Rows may also have *stitch counts*, which show the number of stitches there should be on the needle at the end of the row. There are also *alternate stitch counts*, to allow for the same pattern to be made in different *sizes*.

Patterns may also have *finished measurements*, which is how long the final product should be in different sizes.

A *stitch* has a *name*, an *abbreviation* of that name, and a *symbol*, which is how the stitch is represented in knitting charts. Certain groups of stitches make up a *stitch pattern*, which spans multiple rows but only sometimes the entire length of the row. For example, this is the stitch pattern for a moss stitch:
"
Moss Stitch (worked over an even number of sts) 
Rows 1 and 2: \*K1, p1; rep from * across.
Rows 3 and 4: \*P1, k1; rep from * across.
Rep Rows 1 - 4 for Moss St.
"
Which spans the entire length of multiple rows, while this is a stitch pattern for a cable:
"
Cable (worked over 6 sts)
Row 1 (RS): P1, k4, p1.
Row 2: K1, p4, k1.
Row 3: P1, 2/2 LC, p1.
Row 4: K1, p4, k1.
Rep Rows 1-4 for Left Cable.
"
Stitch patterns tend to differ slightly in the exact number of stitches according to the knitting pattern, but they achieve  the same visual result. Usually any important stitch patterns are described at the top of the pattern.

A pattern may use different *materials* for each part. Materials include *yarn*, which has a *weight*, *color*, *name*, and usually a *shorthand* like "Yarn A" or "(B)" to save space in the pattern; also things like *stitch markers*, whose placement is occasionally noted in patterns. There are also the *needles*. Needles have a *US size*, which is noted in integers, and a *metric size* which is measured in millimeters. The can also be *circular needles*, which have a *cord length*, which is measured in both inches and centimeters.
While a pattern may give a recommended size of needles, the actual size a knitter uses depends upon what size allows the knitter to achieve the specified pattern's *gauge*. Different stitch patterns or sections may have their own gauge.

---------------------------------------------

Models:

Pattern:
    name: str
    sections: list\[Section]
    (extra info)
    creator: str
    yarn: Yarn
    needles: Needle
    final_measurements: list\[str]
    gauge: dict

Section:
    name: str
    caston: int
    pattern: list\[Row]
    (extra)
    parts: list\[Part]

Row:
    number: int
    stitches: list\[Stitch | Repeat]
    stitch_count: int

Stitch:
    name: str
    abbrev: str
    symbol_rs: str
    symbol_ws: str

Repeat:
    elements: list\[Stitch | Repeat]
    has_num_times: bool
    num_times: int
    length: int

-------------------------------------------

Concepts and Terms:

Stitch - A single knitting stitch (k, p, yo, k2tog, etc.)

Repeat - A sequence of stitches and/or repeats that are repeated either a given number of times or until a certain point of the row

Row - A sequence of stitches and/or repeats that make up one row of a knitting pattern

Pattern - A sequence of rows that creates some knitted item

Chart - A visual representation of a written knitting pattern in a grid format

--------------------------------------------