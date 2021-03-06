import time

from curtsies import fmtstr, FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import *

def construct_fmtstr(in_string, out_string, w):
    base_c = gray # Choose base color
    yes_c  = cyan # Choose color when letter typed correctly
    no_c   = red  # Choose color when letter typed incorrectly

    output = ""

    for i in range(len(out_string)):
        if i < len(in_string):
            if in_string[i] == out_string[i]:
                output += yes_c(out_string[i])
            else:
                output += no_c(out_string[i])
        else:
            output += base_c(out_string[i])

    # Gotta do this mess because running .center() on
    # a formatted string removes all of the coloring
    for i in range(len(out_string.center(w))):
        if out_string.center(w)[i] != " ":
            break
        else:
            output = " " + output

    return output

if __name__ == "__main__":
    with FullscreenWindow() as window:
        with Input() as input_generator:
            state = "title"     # We use a state variable to track inputs/outputs depending on program state (title, typing, etc)
            start_time = 0      # Records the start time of a test. Updated when state switched and test begins.
            end_time = 0        # Records the end time of a test. Updated when test is completed.

            a = FSArray(window.height, window.width)

            test_string = "Hello! This is intended to be a test string."

            # These hard-coded values will break with too small a terminal
            a[1, 0] = ["welcome to yet another python typing test.".center(window.width)]
            a[5, 0] = ["            [c] ~ start a Typeracer test."]

            input_string = ""

            window.render_to_terminal(a)

            # All initial construction of screens must be done
            # immediately when input is received; this is because
            # input_generator only gets triggered on a keypress,
            # and as there is only one keypress needed for a change
            # in state, it won't re-run until another key is pressed.
            for c in input_generator:
                if c == '<ESC>':
                    break

                if state == "title":
                    if c == 'c':
                        state = "typing"

                        a = FSArray(window.height, window.width)
                        a[(window.height // 2), 0:len(test_string)] = [construct_fmtstr(input_string, test_string, window.width)]
                        start_time = time.perf_counter()
                        window.render_to_terminal(a)

                elif state == "typing":
                    if c == '<BACKSPACE>':
                        input_string = input_string[:-1]
                    elif c == '<SPACE>':
                        input_string += " "
                    else:
                        input_string += c

                    if input_string == test_string:
                        end_time = time.perf_counter()
                        state = "done"

                        a = FSArray(window.height, window.width)
                        a[1, 0]  = ["well done.~".center(window.width)]
                        a[5, 0]  = [("wpm:    " + str(round(    (len(test_string)/5)    /   ((end_time-start_time)/60),  2))).center(window.width)]
                        a[6, 0]  = [("cpm:    " + str(round(    (len(test_string))    /   ((end_time-start_time)/60),  2))).center(window.width)]
                        a[10, 0] = ["            [c] ~ start another Typeracer test."]
                        window.render_to_terminal(a)
                    else:
                        a = FSArray(window.height, window.width)
                        a[(window.height // 2), 0:len(test_string)] = [construct_fmtstr(input_string, test_string, window.width)]
                        window.render_to_terminal(a)

                elif state == "done":
                    if c == 'c':
                        state = "typing"

                        input_string = ""
                        a = FSArray(window.height, window.width)
                        a[(window.height // 2), 0:len(test_string)] = [construct_fmtstr("", test_string, window.width)]


                        window.render_to_terminal(a)
