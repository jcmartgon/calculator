import customtkinter as ctk
from buttons import Button, NumButton, MathButton
import darkdetect
from settings import *

# Windows OS
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        # setup
        super().__init__(fg_color=(WHITE, BLACK))
        ctk.set_appearance_mode(f"{'dark' if is_dark else 'light'}")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable = (False, False)
        self.title("")
        self.iconbitmap("empty.ico")
        self.title_bar_color(is_dark)

        # grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform="a")
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform="a")

        # data
        self.result_string = ctk.StringVar(value="0")
        self.formula_string = ctk.StringVar(value="")
        self.display_nums = []
        self.full_operation = []

        # widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        """Creates graphical elements"""
        # fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)

        # output labels
        OutputLabel(self, 0, "SE", main_font, self.formula_string)
        OutputLabel(self, 1, "E", result_font, self.result_string)

        # clear (AC) button
        Button(
            parent=self,
            func=self.clear,
            text=OPERATORS["clear"]["text"],
            col=OPERATORS["clear"]["col"],
            row=OPERATORS["clear"]["row"],
            font=main_font,
        )

        # percentage button
        Button(
            parent=self,
            func=self.percent,
            text=OPERATORS["percent"]["text"],
            col=OPERATORS["percent"]["col"],
            row=OPERATORS["percent"]["row"],
            font=main_font,
        )

        # invert button
        Button(
            parent=self,
            func=self.invert,
            text=OPERATORS["invert"]["text"],
            col=OPERATORS["invert"]["col"],
            row=OPERATORS["invert"]["row"],
            font=main_font,
        )

        # number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent=self,
                text=num,
                func=self.num_press,
                col=data["col"],
                row=data["row"],
                font=main_font,
                span=data["span"],
            )

        # operator buttons
        for operator, data in MATH_POSITION.items():
            MathButton(
                parent=self,
                text=data["character"],
                operator=operator,
                func=self.math_press,
                col=data["col"],
                row=data["row"],
                font=main_font,
            )

    def num_press(self, value):
        """Adds value to screen and operation variable"""
        self.display_nums.append(str(value))
        full_number = "".join(self.display_nums)
        self.result_string.set(full_number)

    def math_press(self, value):
        """Updates screen, variables and operates if value is ="""
        current_number = "".join(self.display_nums)

        if current_number:
            self.full_operation.append(current_number)

            if value != "=":
                # update data
                self.full_operation.append(value)
                self.display_nums.clear()

                # update output
                self.result_string.set("")
                self.formula_string.set(" ".join(self.full_operation))
            else:
                formula = " ".join(self.full_operation)
                result = eval(formula)

                # format result
                if isinstance(result, float):
                    # an int is formatted like a float
                    if result.is_integer():
                        result = int(result)
                    else:
                        # handles too many decimals
                        result = round(result, 3)

                # update data
                self.full_operation.clear()

                if result < 0:
                    self.display_nums = ["-", str(result * -1)]
                else:
                    self.display_nums = [str(result)]

                # update output
                self.result_string.set(result)
                self.formula_string.set(formula)

    def clear(self):
        """Clears output and data"""

        # clear output
        self.result_string.set(0)
        self.formula_string.set("")

        # clear data
        self.display_nums.clear()
        self.full_operation.clear()

    def percent(self):
        """Divides the value on screen by 100"""
        if self.display_nums:
            current_number = float("".join(self.display_nums))
            percent_number = current_number / 100

            # handles too many decimals
            percent_number = round(percent_number, 8)

            self.display_nums = list(str(percent_number))
            self.result_string.set("".join(self.display_nums))

    def invert(self):
        """Inverts result's sign"""
        current_number = "".join(self.display_nums)
        if current_number:
            # positive or negative?
            if float(current_number) > 0:
                self.display_nums.insert(0, "-")
            else:
                del self.display_nums[0]

            self.result_string.set("".join(self.display_nums))

    def title_bar_color(self, is_dark):
        """Changes title bar color (dark or light)"""
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = (
                TITLE_BAR_HEX_COLORS["dark"]
                if is_dark
                else TITLE_BAR_HEX_COLORS["light"]
            )
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int)
            )
        except:
            pass


class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)


if __name__ == "__main__":
    Calculator(darkdetect.isDark())
