"""Functions and entities related to rendering a Chart into ASCII"""

import math
from copy import deepcopy
from src.domain.chart.entities.chart import Chart, ChartRow
from src.domain.pattern.entities import StitchType

class ASCIIRender:
    def __init__(self, chart:Chart):
        self.chart = chart

    # PADDING
    # def _pad_grid(self):
    #     og_rows:list[ChartRow] = deepcopy(self.chart.rows)
    #     padded_rows:list[ChartRow] = []
    #     for i, curr_row in enumerate(self.chart.rows):
    #         # print(f"Padding row {curr_row.number}")
    #         if i == 0:
    #             padded_rows.append(curr_row)
    #             continue
            
    #         prev_row = og_rows[i-1]
    #         prev_padded_row = padded_rows[i-1]

    #         prev_unpadded_width = self.chart.pattern.get_row(prev_row.number).num_instructions
    #         curr_unpadded_width = self.chart.pattern.get_row(curr_row.number).num_instructions

    #         # 2. If the current (unpadded) row is longer than the previous (unpadded) row,
    #         #   Add padding to all prior (padded) rows, shorter than the current row
    #         if curr_unpadded_width > prev_unpadded_width:
    #             print(f"Padding scenario 2 on row {curr_row.number}")
    #             # Get all previous shorter rows until encountering one that isn't
    #             previous_rows = og_rows[:i]
    #             previous_rows.reverse()
    #             print(f"previous rows are: {[p_row.number for p_row in previous_rows]}")
    #             shorter_rows:list[ChartRow] = []
    #             last_short_row_idx = 0
    #             for x, unpadded_row in enumerate(previous_rows):
    #                 # print(f"curr_unpadded_width is: {curr_unpadded_width}, prev unpadded width is: {unpadded_row.width}")
    #                 # print(f"prev unpadded row is: {unpadded_row}")
    #                 if curr_unpadded_width > padded_rows[x].width:
    #                     shorter_rows.append(padded_rows[x])
    #                 else:
    #                     if x == 0:
    #                         last_short_row_idx = 0
    #                     else:
    #                         last_short_row_idx = x-1
    #                     break
    #             print(f"Last short row index is: {last_short_row_idx}")
                
    #             # Get which row caused the current row to be longer
    #             relevant_stitches = None
    #             if prev_row.has_increases:
    #                 # print("relevant row is prev row")
    #                 relevant_stitches = self.chart.pattern.get_row(prev_row.number).stitches
    #             elif curr_row.has_increases:
    #                 # print("relevant row is curr row")
    #                 relevant_stitches = self.chart.pattern.get_row(curr_row.number).stitches
                
    #             # Get the amount to pad each shorter row by
    #             middle_point = math.ceil(len(relevant_stitches) / 2)
    #             # print(f"middle point is: {middle_point}")
    #             left_stitches = relevant_stitches[:middle_point]
    #             # print(f"left stitches are: {left_stitches}")
    #             right_stitches = relevant_stitches[middle_point:]
    #             # print(f"right stitches are: {right_stitches}")

    #             to_pad_left = 0
    #             to_pad_right = 0
    #             # TODO: Do some more testing to confirm this works as intended
    #             for stitch in left_stitches:
    #                 if stitch.type == StitchType.INCREASE:
    #                     to_pad_left += (stitch.stitches_produced - stitch.stitches_consumed)
    #                 elif stitch.type == StitchType.DECREASE:
    #                     to_pad_left += (stitch.stitches_produced - stitch.stitches_consumed)    # result is negative, so adding to subtract
    #             for stitch in right_stitches:
    #                 if stitch.type == StitchType.INCREASE:
    #                     to_pad_right += (stitch.stitches_produced - stitch.stitches_consumed)
    #                 elif stitch.type == StitchType.DECREASE:
    #                     to_pad_right += (stitch.stitches_produced - stitch.stitches_consumed)
    #             # print(f"to pad left is: {to_pad_left}. to pad right is: {to_pad_right}")

    #             # Pad shorter rows
    #             padded_shorter_rows = []
    #             for short_row in shorter_rows:
    #                 short_row.pad_row(to_pad_left, to_pad_right)
    #                 padded_shorter_rows.append(short_row)
    #             print(f"padded shorter rows are: {padded_shorter_rows}")
    #             # Update result list
    #             if last_short_row_idx is not None:
    #                 padded_rows[last_short_row_idx:] = padded_shorter_rows

    #         # 3. If the current row is shorter than the previous row,
    #         #   Add padding to the current row on the opposite side of the decrease
    #         if curr_unpadded_width < prev_unpadded_width:
    #             print(f"Padding scenario 3 on row {curr_row.number}")
    #             print(f"curr unpadded width is: {curr_unpadded_width}, prev unpadded width is: {prev_unpadded_width}")

    #             # Get all previous longer rows until encountering one that isn't
    #             previous_rows = og_rows[:i]
    #             previous_rows.reverse()
    #             # print(f"previous rows are: {[p_row.number for p_row in previous_rows]}")
    #             longer_rows:list[ChartRow] = []
    #             last_long_row_idx = 0
    #             for x, unpadded_row in enumerate(previous_rows):
    #                 if curr_unpadded_width < unpadded_row.width:
    #                     longer_rows.append(padded_rows[x])
    #                 else:
    #                     last_long_row_idx = x-1
    #                     break
                
    #             # Get which row caused the current row to be shorter
    #             relevant_stitches = None
    #             if prev_row.has_decreases:
    #                 # print("relevant row is prev row")
    #                 relevant_stitches = self.chart.pattern.get_row(prev_row.number).stitches
    #             elif curr_row.has_decreases:
    #                 # print("relevant row is curr row")
    #                 relevant_stitches = self.chart.pattern.get_row(curr_row.number).stitches
                
    #             # Get the amount to pad each shorter row by
    #             middle_point = math.ceil(len(relevant_stitches) / 2)
    #             print(f"middle point is: {middle_point}")
    #             left_stitches = relevant_stitches[:middle_point]
    #             print(f"left stitches are: {left_stitches}")
    #             right_stitches = relevant_stitches[middle_point:]
    #             print(f"right stitches are: {right_stitches}")

    #             to_pad_left = 0
    #             to_pad_right = 0
    #             # TODO: Do some more testing to confirm this works as intended
    #             for stitch in left_stitches:
    #                 if stitch.type == StitchType.INCREASE:
    #                     to_pad_right -= (stitch.stitches_produced - stitch.stitches_consumed)
    #                 elif stitch.type == StitchType.DECREASE:
    #                     to_pad_right -= (stitch.stitches_produced - stitch.stitches_consumed)   # result is negative, so subtracting to add
    #             for stitch in right_stitches:
    #                 if stitch.type == StitchType.INCREASE:
    #                     to_pad_left -= (stitch.stitches_produced - stitch.stitches_consumed)
    #                 elif stitch.type == StitchType.DECREASE:
    #                     to_pad_left -= (stitch.stitches_produced - stitch.stitches_consumed)
    #             print(f"to pad left is: {to_pad_left}. to pad right is: {to_pad_right}")

    #             curr_row.pad_row(to_pad_left, to_pad_right)

    #         # 1. If the current row is shorter than the chart's width AND the previous row has padding
    #         #   Add equal amount of padding to the current row
    #         if curr_row.width < self.chart.width and prev_padded_row.has_padding:
    #             print(f"Padding scenario 1 on row {curr_row.number}")
    #             print(f"curr row width is {curr_row.width}")
    #             padding = prev_padded_row.get_padding_counts()
    #             curr_row.pad_row(padding["left"], padding["right"])

    #         padded_rows.append(curr_row)
    #         print(f"added row {curr_row.number}, len of padded rows is: {len(padded_rows)}")
    #         # print(f"padded rows are: {padded_rows}")

    #     return padded_rows
            
    # def _pad_grid(self):
    #     og_rows:list[ChartRow] = deepcopy(self.chart.rows)
    #     padded_rows:list[ChartRow] = []
    #     for i, curr_row in enumerate(self.chart.rows):
    #         if i == 0:
    #             padded_rows.append(curr_row)
    #             continue

    #         # if previous row was shorter
    #         prev_row = padded_rows[i-1]
    #         curr_stitches = self.chart.pattern.get_row(curr_row.number).stitches
    #         prev_stitches = self.chart.pattern.get_row(prev_row.number).stitches
    #         if curr_row.width > prev_row.width:
    #             print(f"Increase scenario found on row {curr_row.number}")
    #             # Calculate how much needs to be padded
    #             to_be_padded = curr_row.width - prev_row.width
    #             print(f"{to_be_padded} padding needed")

    #             # Figure out which row caused curr_row to be longer
    #             ## TODO: Probably needs to be changed
    #             curr_expanded_row = self.chart.pattern.get_row(curr_row.number)
    #             prev_expanded_row = self.chart.pattern.get_row(prev_row.number)

    #             relevant_row = None
    #             relevant_stitches = None
    #             if curr_expanded_row.ended_longer:
    #                 relevant_row = curr_row
    #                 relevant_stitches = curr_stitches
    #             elif prev_expanded_row.ended_longer:
    #                 relevant_row = prev_row
    #                 relevant_stitches = prev_stitches
    #             else:
    #                 raise ValueError("Something went wrong when trying to calculate relevant padding row in an increase scenario")

    #             # Calculate where it needs to be padded
    #             middle_point = math.ceil(relevant_row.width / 2)
    #             left_stitches = relevant_stitches[:middle_point]
    #             right_stitches = relevant_stitches[middle_point:]
    #             print(f"left stitches are: {left_stitches}, right stitches are: {right_stitches}")

    #             to_pad_left = 0
    #             to_pad_right = 0
    #             for stitch in left_stitches:
    #                 if (stitch.type == StitchType.INCREASE) or (stitch.type == StitchType.DECREASE):
    #                     to_pad_right += (stitch.stitches_produced - stitch.stitches_consumed)
    #             for stitch in right_stitches:
    #                 if (stitch.type == StitchType.INCREASE) or (stitch.type == StitchType.DECREASE):
    #                     to_pad_left += (stitch.stitches_produced - stitch.stitches_consumed)
                
    #             if to_pad_left + to_pad_right != to_be_padded:
    #                 raise ValueError(
    #                     f"Something went wrong when calculating padding:\n" \
    #                     f"To be padded is: {to_be_padded}. " \
    #                     f"To pad left is: {to_pad_left} and to pad right is: {to_pad_right}"
    #                 )
                
    #             # Pad
    #             prev_row.pad_row(to_pad_left, to_pad_right)
    #             padded_rows[i-1] = prev_row

    #         padded_rows.append(curr_row)

    #     return padded_rows

    # PUTTING GRID TOGETHER
    def _build_border(self) -> str:
        """Create the border line to the width of the chart"""
        # Calculate many dashes there should be per item
        length = self.chart.pattern.get_max_length()
        dash_num = self.chart.get_max_cell_length() + 2 # +2 for the padding on either side

        # Build border
        border_line = "-" * dash_num
        border = border_line
        for _ in range(length + 1): # +1 is for the last space 
            border += f"+{border_line}"

        return border + "\n"
