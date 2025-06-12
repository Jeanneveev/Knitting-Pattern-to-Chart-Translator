The planned user workflow is that the user inputs their pattern, that pattern gets parsed into a dict of lists, each representing one row of the pattern. Each stitch in each row of that dict then gets translated into their corresponding symbol, which is then displayed as a chart.

Thus, the project has 3 major parts:
1. The parser which parses knitting patterns to a dictionary
2. A second parser (?) or a model that translates the stitches in the dictionary to their corresponding symbols
3. The UI which will display the chart

I decided to partially combine 1 and 2 so that the parser directly outputs the model's classes.
So now, the major parts are:
1. The parser which parses knitting patterns to corresponding class instances
2. 