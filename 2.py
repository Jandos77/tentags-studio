import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser, filedialog


class CellProperties(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Cell A1")

        self.build()

    def build(self):

        pad = 8

        # ---------------------------------------------------------
        # Text
        # ---------------------------------------------------------

        ttk.Label(self, text="Text").pack(anchor="w", padx=pad, pady=(10, 2))

        self.text = tk.Text(
            self,
            height=4,
            width=28
        )

        self.text.pack(fill="x", padx=pad)

        # ---------------------------------------------------------
        # Bold / Italic
        # ---------------------------------------------------------

        row = ttk.Frame(self)
        row.pack(fill="x", padx=pad, pady=8)

        self.bold = tk.BooleanVar()

        ttk.Checkbutton(
            row,
            text="Bold",
            variable=self.bold
        ).pack(side="left")

        self.italic = tk.BooleanVar()

        ttk.Checkbutton(
            row,
            text="Italic",
            variable=self.italic
        ).pack(side="left", padx=20)

        # ---------------------------------------------------------
        # Alignment
        # ---------------------------------------------------------

        ttk.Label(self, text="Alignment").pack(anchor="w", padx=pad)

        self.align = ttk.Combobox(
            self,
            values=[
                "Left",
                "Center",
                "Right"
            ],
            state="readonly"
        )

        self.align.current(0)
        self.align.pack(fill="x", padx=pad, pady=4)

        # ---------------------------------------------------------
        # Text color
        # ---------------------------------------------------------

        ttk.Label(self, text="Text Color").pack(anchor="w", padx=pad)

        row = ttk.Frame(self)
        row.pack(fill="x", padx=pad)

        self.text_color = "#000000"

        self.text_preview = tk.Label(
            row,
            bg=self.text_color,
            width=4,
            relief="solid"
        )

        self.text_preview.pack(side="left")

        ttk.Button(
            row,
            text="Choose...",
            command=self.choose_text_color
        ).pack(side="left", padx=8)

        # ---------------------------------------------------------
        # Background
        # ---------------------------------------------------------

        ttk.Label(self, text="Background").pack(anchor="w", padx=pad, pady=(10, 0))

        row = ttk.Frame(self)
        row.pack(fill="x", padx=pad)

        self.bg_color = "#ffffff"

        self.bg_preview = tk.Label(
            row,
            bg=self.bg_color,
            width=4,
            relief="solid"
        )

        self.bg_preview.pack(side="left")

        ttk.Button(
            row,
            text="Choose...",
            command=self.choose_bg_color
        ).pack(side="left", padx=8)

        # ---------------------------------------------------------
        # URL
        # ---------------------------------------------------------

        ttk.Label(self, text="URL").pack(anchor="w", padx=pad, pady=(10, 2))

        self.url = ttk.Entry(self)

        self.url.pack(fill="x", padx=pad)

        # ---------------------------------------------------------
        # Mark
        # ---------------------------------------------------------

        ttk.Label(self, text="Mark").pack(anchor="w", padx=pad, pady=(10, 2))

        self.mark = ttk.Entry(self)

        self.mark.pack(fill="x", padx=pad)

        # ---------------------------------------------------------
        # Image
        # ---------------------------------------------------------

        ttk.Label(self, text="Image").pack(anchor="w", padx=pad, pady=(10, 2))

        row = ttk.Frame(self)
        row.pack(fill="x", padx=pad)

        self.image = ttk.Entry(row)

        self.image.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            row,
            text="Browse...",
            command=self.select_image
        ).pack(side="left", padx=6)

        # ---------------------------------------------------------
        # Image Size
        # ---------------------------------------------------------

        row = ttk.Frame(self)
        row.pack(fill="x", padx=pad, pady=8)

        ttk.Label(row, text="W").grid(row=0, column=0)

        self.w = ttk.Entry(row, width=6)
        self.w.insert(0, "120")
        self.w.grid(row=0, column=1)

        ttk.Label(row, text="H").grid(row=0, column=2, padx=(10, 0))

        self.h = ttk.Entry(row, width=6)
        self.h.insert(0, "auto")
        self.h.grid(row=0, column=3)

        ttk.Label(row, text="M").grid(row=0, column=4, padx=(10, 0))

        self.m = ttk.Entry(row, width=6)
        self.m.insert(0, "15")
        self.m.grid(row=0, column=5)

        # ---------------------------------------------------------
        # Merge
        # ---------------------------------------------------------

        ttk.Label(self, text="Merge").pack(anchor="w", padx=pad)

        ttk.Button(
            self,
            text="Merge Right"
        ).pack(fill="x", padx=pad, pady=3)

        ttk.Button(
            self,
            text="Merge Down"
        ).pack(fill="x", padx=pad)

        ttk.Button(
            self,
            text="Unmerge"
        ).pack(fill="x", padx=pad, pady=(3, 10))

        # ---------------------------------------------------------
        # Apply
        # ---------------------------------------------------------

        ttk.Separator(self).pack(fill="x", pady=8)

        ttk.Button(
            self,
            text="Apply"
        ).pack(
            fill="x",
            padx=pad,
            pady=(0, 10)
        )

    # =========================================================

    def choose_text_color(self):

        color = colorchooser.askcolor(
            self.text_color
        )[1]

        if color:
            self.text_color = color
            self.text_preview.configure(bg=color)

    def choose_bg_color(self):

        color = colorchooser.askcolor(
            self.bg_color
        )[1]

        if color:
            self.bg_color = color
            self.bg_preview.configure(bg=color)

    def select_image(self):

        filename = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp")
            ]
        )

        if filename:
            self.image.delete(0, "end")
            self.image.insert(0, filename)


# ==========================================================
# Demo
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("Cell Properties")

    panel = CellProperties(root)

    panel.pack(fill="y", padx=10, pady=10)

    root.mainloop()