from src.domain.services.make_pattern import Pattern, ExpandedRow
from src.domain.model.model import Stitch, StitchType
import math

class Chart:
    def __init__(self, pattern:Pattern):
        self.pattern = pattern

    def get_row_symbols(self, row_num:int) -> list[str]:
        """Get the symbols of a row in the pattern by its row number"""
        ## NOTE: odd rows are on the right side and use rs symbols
        # while even rows are on the wrong side and use ws symbols.
        if row_num % 2 == 1:  #right-side, display in reverse
            # print("right-side")
            row = self.pattern.get_row(row_num)
            symbols = row.get_symbols_rs()
            symbols.reverse()
            return symbols
        else:   #wrong-side, display normally
            # print("wrong-side")
            row = self.pattern.get_row(row_num)
            symbols = row.get_symbols_ws()
            return symbols
        
    def _get_max_item_length(self) -> int:
        """Get the longest item in the chart +2 for padding"""
        symbols_used = self.pattern.get_symbols_used()
        max_sym_len = 0
        
        for symbol in symbols_used:
            sym_len = len(symbol)
            if "\\" in symbol:
                sym_len - 1
            max_sym_len = max(sym_len, max_sym_len)

        last_row_num = self.pattern.rows[-1].number
        longest_item = max(max_sym_len, len(str(last_row_num)))
        longest_item += 2    # for the spacing on either side

        return longest_item
        
    def _build_border(self) -> str:
        # Calculate many dashes there should be per item
        length = self.pattern.get_max_length()
        dash_num = self._get_max_item_length()

        # Build border
        border_line = "-" * dash_num
        border = border_line
        for _ in range(length + 1): # +1 is for the last space 
            border += f"+{border_line}"

        return border + "\n"
    
    def _pad_item(self, symbol:str):
        item_len = self._get_max_item_length()
        sym_len = len(symbol)
        to_pad = item_len - sym_len # always < 2

        padded_item = symbol
        for i in range(to_pad):
            if i % 2 == 0:
                padded_item = " " + padded_item
            else:
                padded_item = padded_item + " "

        return padded_item
    
    def _build_row_from_symbols(self, symbols:list[str], row_num:int) -> str:
        # print(f"building row {row_num}")
        result = "|"
        # print(f"symbols are now: {symbols}")
        
        for symbol in symbols:
            padded = self._pad_item(symbol)
            result += f"{padded}|"

        padded_row_num = self._pad_item(str(row_num))
        space = " " * len(padded_row_num)
        if row_num % 2 == 1:    #right-side, display in reverse
            # print("right-side")
            result = space + result + f"{padded_row_num}"
        else:               #wrong-side, display normally
            # print("wrong-side")
            result = f"{padded_row_num}" + result + space

        return result + "\n"
    
    def _check_padding_sides(self, symbols:list[str]) -> dict:
        """Get the count on each side of all, if any, padding stitches in the given row"""
        all_padding = {"left":0, "right":0}
        # NOTE: The index of where the Xs stop is also the number of Xs there are
        all_padding["left"] = next(i for i, symbol in enumerate(symbols) if symbol != "X")
        all_padding["right"] = next(i for i, symbol in enumerate(list(reversed(symbols))) if symbol != "X")
        
        return all_padding

    def _pad_all_shorter_rows(self, shorter_rows:dict[int, list[str]], to_pad_left, to_pad_right) -> dict:
        result = {}
        for i, short_row_padded_symbols in shorter_rows.items():
            for _ in range(to_pad_left):
                    short_row_padded_symbols.insert(0, "X")
            for _ in range(to_pad_right):
                short_row_padded_symbols.insert(len(short_row_padded_symbols), "X")    

            result[i] = short_row_padded_symbols
        return result

    def _pad_grid(self):
        expanded_rows = self.pattern.rows
        padded_symbols_rows:list[list[str]] = []
        for i, curr_row in enumerate(expanded_rows):
            # print(f"padding row {curr_row.number}")
            if i == 0:
                padded_symbols_rows.append(self.get_row_symbols(curr_row.number))
                continue
        
            prev_row = expanded_rows[i-1]
            # prev_unpadded_symbols = self.get_row_symbols(prev_row.number)
            prev_padded_symbols = padded_symbols_rows[i-1]
            prev_unpadded_len = prev_row.num_instructions
            curr_unpadded_len = curr_row.num_instructions
            curr_symbols = self.get_row_symbols(curr_row.number)
        
            # 1. If the current row is shorter than the maximum length AND the previous row has padding
            #   add equal amount of padding on current row
            prev_padding_side_counts = self._check_padding_sides(prev_padded_symbols)
            # print(f"prev padding side counts of row {prev_row.number} are {prev_padding_side_counts}")
            prev_left_padding_count = prev_padding_side_counts["left"]
            prev_right_padding_count = prev_padding_side_counts["right"]
            if (
                (len(curr_symbols) < self.pattern.get_max_length()) and
                (prev_left_padding_count != 0) and (prev_right_padding_count != 0)
            ):
                # print(f"Padding scenario 1")
                for _ in range(prev_left_padding_count):
                    curr_symbols.insert(0, "X")
                for _ in range(prev_right_padding_count):
                    curr_symbols.insert(len(curr_symbols), "X")

            # 2. If the current row is longer than the previous row,
            #   Add padding to all prior rows that are shorter than this row until you reach one that isn't
            if curr_unpadded_len > prev_unpadded_len:
                # print("Padding scenario 2")

                # Get all previous shorter rows until encountering one that isn't
                shorter_rows: dict = {}
                for x, row in enumerate(expanded_rows):
                    if curr_unpadded_len > row.num_instructions:
                        # print(f"Row {row.number} is shorter than row {curr_row.number}")
                        shorter_rows[x] = padded_symbols_rows[x]
                    else:
                        break
                # Get the amount to pad each shorter row by
                relevant_row = None
                if any(st for st in prev_row.stitches if st.type == StitchType.INCREASE):
                    relevant_row = prev_row
                elif any(st for st in curr_row.stitches if st.type == StitchType.INCREASE):
                    relevant_row = curr_row

                middle_point = math.ceil(relevant_row.num_instructions / 2)
                left_stiches = relevant_row.stitches[:middle_point]
                right_stiches = relevant_row.stitches[middle_point:]
                to_pad_left = 0
                to_pad_right = 0
                for stitch in left_stiches:
                    # print(f"reading stitch {stitch}")
                    if stitch.type == StitchType.INCREASE:
                        # print("Increase found on left")
                        to_pad_left += (stitch.stitches_produced - stitch.stitches_consumed)
                    elif stitch.type == StitchType.DECREASE:
                        to_pad_left += (stitch.stitches_produced - stitch.stitches_consumed)
                for stitch in right_stiches:
                    if stitch.type == StitchType.INCREASE:
                        # print("Increase found on right")
                        to_pad_right += (stitch.stitches_produced - stitch.stitches_consumed)
                    elif stitch.type == StitchType.DECREASE:
                        to_pad_right += (stitch.stitches_produced - stitch.stitches_consumed)
                # print(f"to pad left is: {to_pad_left}, to pad right is: {to_pad_right}")

                changed_rows = self._pad_all_shorter_rows(shorter_rows, to_pad_left, to_pad_right)
                for key, value in changed_rows.items():
                    padded_symbols_rows[key] = value
                    # print(f"row updated, is now {value}")

                
            # 3. If the current row is shorter than the previous row,
            #   add padding to the current row on the oppsite side of the decrease
            if curr_unpadded_len < prev_unpadded_len:
                # print("Padding scenario 3")

                # Get all previous longer rows until encountering one that isn't
                longer_rows: dict = {}
                for x, row in enumerate(expanded_rows):
                    if curr_unpadded_len < row.num_instructions:
                        # print(f"Row {row.number} is longer than row {curr_row.number}")
                        longer_rows[x] = padded_symbols_rows[x]
                    else:
                        break
                # Get the amount to pad current row by
                middle_point = math.ceil(curr_row.num_instructions / 2)
                left_stiches = curr_row.stitches[:middle_point]
                right_stiches = curr_row.stitches[middle_point:]
                # if curr_row.number == 12: print(f"middle point is at {middle_point}. left stitches are {left_stiches}. right stitches are {right_stiches}")
                to_pad_left = 0
                to_pad_right = 0
                for stitch in left_stiches:
                    if stitch.type == StitchType.INCREASE:
                        to_pad_left -= (stitch.stitches_produced - stitch.stitches_consumed)
                    elif stitch.type == StitchType.DECREASE:
                        to_pad_left -= (stitch.stitches_produced - stitch.stitches_consumed)
                for stitch in right_stiches:
                    if stitch.type == StitchType.INCREASE:
                        to_pad_right -= (stitch.stitches_produced - stitch.stitches_consumed)
                    elif stitch.type == StitchType.DECREASE:
                        to_pad_right -= (stitch.stitches_produced - stitch.stitches_consumed)

                # NOTE: Probably should be changed later
                if not right_stiches:
                    to_pad_right = int(to_pad_left / 2)
                    to_pad_left = int(to_pad_left / 2)
                if not left_stiches:
                    to_pad_left = int(to_pad_right / 2)
                    to_pad_right = int(to_pad_right / 2)

                for _ in range(to_pad_left):
                    curr_symbols.insert(0, "X")
                for _ in range(to_pad_right):
                    curr_symbols.insert(len(curr_symbols), "X")

            padded_symbols_rows.append(curr_symbols)

        return list(reversed(padded_symbols_rows))

    def render_grid(self):
        padded_symbols_grid = self._pad_grid()
        row_nums = [row.number for row in list(reversed(self.pattern.rows))]
        body = []
        border = self._build_border()
        for i, padded_symbols_row in enumerate(padded_symbols_grid):
            body.append(self._build_row_from_symbols(padded_symbols_row, row_nums[i]))

        grid = ""
        for row in body:
            grid += border
            grid += row
        grid += border

        # print(f"grid is:\n {grid}")
        return grid

    
    def _get_column_width(self, contents:list[str]) -> int:
        """Get the width of the longest value in the column"""
        max_width = 0
        for string in contents:
            max_width = max(max_width, len(string))

        return max_width + 2    # +2 for padding
    
    def _pad_column(self, column_contents) -> list[str]:
        column_width = self._get_column_width(column_contents)
        padded_contents = []
        for content in column_contents:
            text_width = len(content)
            if (column_width - text_width) % 2 == 0:
                space_width = int((column_width - text_width) / 2)
                padding = " " * space_width
                padded_contents.append(padding + content + padding) 
            else:
                space_width = int((column_width - text_width - 1) / 2)
                padding_left = " " * (space_width + 1)
                padding_right = " " * space_width
                padded_contents.append(padding_left + content + padding_right)

        return padded_contents
    
    def render_key(self) -> str:
        key = ""
        names = []
        right_sides = []
        wrong_sides = []
        abbreviations = self.pattern.get_stitches_used()
        for stitch in abbreviations:
            stitch_info = Stitch.STITCH_BY_ABBREV[stitch]
            names.append(stitch_info.get("name").title())
            right_sides.append(stitch_info.get("rs"))
            wrong_sides.append(stitch_info.get("ws"))
        
        names.insert(0, "Name")
        abbreviations.insert(0, "Abbrev")
        right_sides.insert(0, "RS Symbol")
        wrong_sides.insert(0, "WS Symbol")
        
        name_col_width = self._get_column_width(names)
        abbrev_col_width = self._get_column_width(abbreviations)
        rs_col_width = self._get_column_width(right_sides)
        ws_col_width = self._get_column_width(wrong_sides)

        names_padded = self._pad_column(names)
        abbrev_padded = self._pad_column(abbreviations)
        rs_padded = self._pad_column(right_sides)
        ws_padded = self._pad_column(wrong_sides)

        border = (
            "+" + ("-" * name_col_width) +
            "+" + ("-" * abbrev_col_width) +
            "+" + ("-" * rs_col_width) +
            "+" + ("-" * ws_col_width) +
            "+" + "\n"
        )

        key += border
        for idx in range(len(abbreviations)):
            key += (
                "|" + names_padded[idx] +
                "|" + abbrev_padded[idx] +
                "|" + rs_padded[idx] +
                "|" + ws_padded[idx] +
                "|" + "\n"
            )
            key += border

        return key