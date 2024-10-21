import zpl


class ZPLLabel(zpl.Label):
    def __init__(self, width: float, height: float, printer_settings: dict):
        self.x_offset = printer_settings["x_offset"]
        self.y_offset = printer_settings["y_offset"]
        super().__init__(width=width, height=height)

    def add_box(
            self,
            x: float,
            y: float,
            width: float,
            height: float,
            thickness: float = 2,
            color: str = "B",
            rounding: int = 0,
    ):
        self.origin(x=x + self.x_offset, y=y + self.y_offset)
        self.draw_box(
            width=width,
            height=height,
            thickness=thickness,
            color=color,
            rounding=rounding,
        )
        self.endorigin()

    def add_text(
            self,
            x: float,
            y: float,
            text: str | float,
            font: str,
            char_height: float,
            char_width: float,
            orientation: str = "N",
            change_international_font: float | None = None,
            reverse: bool = False,
    ) -> None:
        if reverse:
            self.reverse_print("Y")
        self.origin(x=x + self.x_offset, y=y + self.y_offset)
        if change_international_font:
            self.change_international_font(character_set=change_international_font)
        self.write_text(
            text=text,
            font=font,
            char_height=char_height,
            char_width=char_width,
            orientation=orientation,
        )
        self.endorigin()
        if reverse:
            self.reverse_print("N")

    def add_qr(
            self,
            x: float,
            y: float,
            code: str,
            error_correction: str,
            magnification: int,
    ) -> None:
        self.origin(x=x + self.x_offset, y=y + self.y_offset)
        self.barcode(
            barcode_type="Q",
            code=code,
            errorCorrection=error_correction,
            magnification=magnification,
        )
        self.endorigin()
