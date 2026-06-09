from tkinter import *
from tkinter import messagebox
import random
import os
import json

# ── Window setup ──────────────────────────────────────────────────────────────
win = Tk()
win.title("Billing Software")
win.resizable(True, True)

screen_w = win.winfo_screenwidth()
screen_h = win.winfo_screenheight()
win.geometry(f"{screen_w}x{screen_h}+0+0")

try:
    win.state("zoomed")
except Exception:
    try:
        win.attributes("-zoomed", True)
    except Exception:
        pass

_scale = min(screen_w / 1366, screen_h / 768)
def fs(size):
    return max(8, int(size * _scale))

SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
BILLS_DIR      = os.path.join(SCRIPT_DIR, "bills")
CUSTOMERS_FILE = os.path.join(SCRIPT_DIR, "customers.json")

BG       = "red"
FG_WHITE = "white"
FG_ITEM  = "lightgreen"
FG_ENTRY = "blue"
FG_GOLD  = "Gold"

# ── Price catalogue ───────────────────────────────────────────────────────────
CATEGORIES = {
    "cosmetics": {
        "Bath Soap":   10,
        "Face Cream":  20,
        "Face Wash":   10,
        "Hair Spray":  25,
        "Hair Gel":    15,
        "Body Lotion": 35,
    },
    "grocery": {
        "Rice":      30,
        "Food Oil": 100,
        "Daal":     100,
        "Wheat":     18,
        "Sugar":     38,
        "Tea":       50,
    },
    "cold_drink": {
        "Maaza":     40,
        "Coca Cola": 40,
        "Frooti":    40,
        "Thumbs Up": 40,
        "Limka":     40,
        "Sprite":    40,
    },
}

qty_vars = {
    cat: {item: IntVar() for item in items}
    for cat, items in CATEGORIES.items()
}

bill_num = random.randint(1000, 9999)

# ── Customer database helpers ─────────────────────────────────────────────────
def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE) as fh:
            return json.load(fh)
    return {}

def save_customers(db):
    with open(CUSTOMERS_FILE, "w") as fh:
        json.dump(db, fh, indent=2)

# ── Business logic ────────────────────────────────────────────────────────────
def calc_subtotal(category):
    return sum(
        qty_vars[category][item].get() * price
        for item, price in CATEGORIES[category].items()
    )

def _get_float(entry):
    try:
        return float(entry.get())
    except ValueError:
        return 0.0

def refresh_totals():
    global bill_num
    bill_num = random.randint(1000, 9999)
    cbill_txt.delete(0, END)
    cbill_txt.insert(0, bill_num)

    for cat, m_entry, c_entry in [
        ("cosmetics",  m1_txt, c1_txt),
        ("grocery",    m2_txt, c2_txt),
        ("cold_drink", m3_txt, c3_txt),
    ]:
        sub = calc_subtotal(cat)
        tax = round(sub * 0.18, 2)
        m_entry.delete(0, END)
        m_entry.insert(0, sub)
        c_entry.delete(0, END)
        c_entry.insert(0, tax)

def generate_bill():
    if not cname.get().strip():
        messagebox.showwarning("Missing Info", "Please enter customer name.")
        return
    refresh_totals()

    sub = {cat: _get_float(e) for cat, e in zip(
        ["cosmetics", "grocery", "cold_drink"], [m1_txt, m2_txt, m3_txt])}
    tax = {cat: _get_float(e) for cat, e in zip(
        ["cosmetics", "grocery", "cold_drink"], [c1_txt, c2_txt, c3_txt])}
    grand_total = sum(sub.values()) + sum(tax.values())

    bill_area.delete(1.0, END)
    bill_area.insert(END, "    *** Welcome to Retail Store ***\n")
    bill_area.insert(END, f"  Bill No  : {bill_num}\n")
    bill_area.insert(END, f"  Name     : {cname.get()}\n")
    bill_area.insert(END, f"  Phone    : {cnum.get()}\n")
    bill_area.insert(END, "=" * 40 + "\n")
    bill_area.insert(END, f"  {'Product':<24}{'Price':>8}\n")
    bill_area.insert(END, "=" * 40 + "\n")
    bill_area.insert(END, f"  {'Cosmetics':<24}{sub['cosmetics']:>8.2f}\n")
    bill_area.insert(END, f"  {'Grocery':<24}{sub['grocery']:>8.2f}\n")
    bill_area.insert(END, f"  {'Cold Drinks':<24}{sub['cold_drink']:>8.2f}\n")
    bill_area.insert(END, "-" * 40 + "\n")
    bill_area.insert(END, f"  {'Tax 18% - Cosmetics':<24}{tax['cosmetics']:>8.2f}\n")
    bill_area.insert(END, f"  {'Tax 18% - Grocery':<24}{tax['grocery']:>8.2f}\n")
    bill_area.insert(END, f"  {'Tax 18% - Cold Drinks':<24}{tax['cold_drink']:>8.2f}\n")
    bill_area.insert(END, "=" * 40 + "\n")
    bill_area.insert(END, f"  {'TOTAL':<24}{grand_total:>8.2f}\n")
    bill_area.insert(END, "=" * 40 + "\n")
    bill_area.insert(END, "\n       Authorized Signature\n")

    _prompt_save(sub, tax, grand_total)

def _prompt_save(sub, tax, grand_total):
    if not messagebox.askyesno("Save Bill", "Save this bill?"):
        return
    os.makedirs(BILLS_DIR, exist_ok=True)
    num = cbill_txt.get()

    # Save text bill
    txt_path = os.path.join(BILLS_DIR, f"{num}.txt")
    with open(txt_path, "w") as fh:
        fh.write(bill_area.get(1.0, END))

    # Save structured JSON bill
    bill_data = {
        "bill_num": num,
        "name": cname.get().strip(),
        "phone": cnum.get().strip(),
        "quantities": {
            cat: {item: qty_vars[cat][item].get() for item in CATEGORIES[cat]}
            for cat in CATEGORIES
        },
        "subtotals": sub,
        "taxes": tax,
        "grand_total": round(grand_total, 2),
    }
    json_path = os.path.join(BILLS_DIR, f"{num}.json")
    with open(json_path, "w") as fh:
        json.dump(bill_data, fh, indent=2)

    # Update customer database keyed by phone number
    phone = cnum.get().strip()
    if phone:
        db = load_customers()
        db[phone] = {"name": cname.get().strip(), "last_bill": num}
        save_customers(db)

    messagebox.showinfo("Saved", "Bill saved successfully!")

def search_bill():
    num = cbill_txt.get().strip()
    if not num:
        messagebox.showwarning("Search", "Enter a bill number to search.")
        return

    json_path = os.path.join(BILLS_DIR, f"{num}.json")
    txt_path  = os.path.join(BILLS_DIR, f"{num}.txt")

    if os.path.exists(json_path):
        with open(json_path) as fh:
            data = json.load(fh)

        # Restore customer details
        cname_txt.delete(0, END)
        cname_txt.insert(0, data.get("name", ""))
        ccont_txt.delete(0, END)
        ccont_txt.insert(0, data.get("phone", ""))

        # Restore all quantities
        for cat, items in data.get("quantities", {}).items():
            for item, qty in items.items():
                if cat in qty_vars and item in qty_vars[cat]:
                    qty_vars[cat][item].set(qty)

        # Restore totals entries
        sub = data.get("subtotals", {})
        tax = data.get("taxes", {})
        for entry, key in zip([m1_txt, m2_txt, m3_txt],
                               ["cosmetics", "grocery", "cold_drink"]):
            entry.delete(0, END)
            entry.insert(0, sub.get(key, ""))
        for entry, key in zip([c1_txt, c2_txt, c3_txt],
                               ["cosmetics", "grocery", "cold_drink"]):
            entry.delete(0, END)
            entry.insert(0, tax.get(key, ""))

        # Show text bill if available
        bill_area.delete(1.0, END)
        if os.path.exists(txt_path):
            with open(txt_path) as fh:
                bill_area.insert(END, fh.read())
        else:
            bill_area.insert(END, f"Bill #{num} loaded from JSON.\n")
        return

    if os.path.exists(txt_path):
        bill_area.delete(1.0, END)
        with open(txt_path) as fh:
            bill_area.insert(END, fh.read())
        return

    messagebox.showerror("Not Found", f"No bill found for #{num}.")

def phone_autofill(event=None):
    """Look up the entered phone number and autofill customer name if known."""
    phone = cnum.get().strip()
    if not phone:
        return
    db = load_customers()
    if phone in db:
        current_name = cname.get().strip()
        if not current_name:
            cname_txt.delete(0, END)
            cname_txt.insert(0, db[phone]["name"])

def clear():
    global bill_num
    bill_num = random.randint(1000, 9999)
    bill_area.delete(1.0, END)
    cname_txt.delete(0, END)
    ccont_txt.delete(0, END)
    cbill_txt.delete(0, END)
    for cat in qty_vars.values():
        for var in cat.values():
            var.set(0)
    for entry in (m1_txt, m2_txt, m3_txt, c1_txt, c2_txt, c3_txt):
        entry.delete(0, END)

# ── UI construction ───────────────────────────────────────────────────────────

Label(
    win, text="Billing Software", bd=8,
    font=("Times New Roman", fs(26), "bold"),
    relief=GROOVE, bg=BG, fg="yellow", pady=4,
).pack(fill=X)

f_cust = LabelFrame(
    win, text="Customer Details",
    font=("Times New Roman", fs(10), "bold"),
    fg=FG_GOLD, bg=BG, bd=8, relief=GROOVE,
)
f_cust.pack(fill=X, padx=5, pady=2)
for col in range(8):
    f_cust.columnconfigure(col, weight=1)

Label(f_cust, text="Customer Name :",
      font=("Times New Roman", fs(13), "bold"), fg=FG_WHITE, bg=BG
      ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
cname = StringVar()
cname_txt = Entry(f_cust, font=("Times New Roman", fs(11), "bold"),
                  textvariable=cname, fg=FG_ENTRY, bd=5)
cname_txt.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

Label(f_cust, text="Contact No :",
      font=("Times New Roman", fs(13), "bold"), fg=FG_WHITE, bg=BG
      ).grid(row=0, column=2, padx=10, pady=5, sticky="e")
cnum = StringVar()
ccont_txt = Entry(f_cust, font=("Times New Roman", fs(11), "bold"),
                  textvariable=cnum, fg=FG_ENTRY, bd=5)
ccont_txt.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

# Autofill name when phone number is entered
ccont_txt.bind("<Return>",    phone_autofill)
ccont_txt.bind("<FocusOut>",  phone_autofill)

Label(f_cust, text="Bill No :",
      font=("Times New Roman", fs(13), "bold"), fg=FG_WHITE, bg=BG
      ).grid(row=0, column=4, padx=10, pady=5, sticky="e")
cbill_num = StringVar()
cbill_txt = Entry(f_cust, font=("Times New Roman", fs(11), "bold"),
                  textvariable=cbill_num, fg=FG_ENTRY, bd=5, width=10)
cbill_txt.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

Button(f_cust, text="Search", command=search_bill,
       font=("Times New Roman", fs(11), "bold"),
       fg=FG_ENTRY, bg="yellow", bd=5,
       ).grid(row=0, column=6, padx=10, pady=5)

# ── Bottom: totals summary + action buttons ───────────────────────────────────
f_menu = LabelFrame(win, text="Bill Menu", relief=GROOVE,
                    font=("Times New Roman", fs(10), "bold"),
                    fg=FG_GOLD, bg=BG, bd=8)
f_menu.pack(side=BOTTOM, fill=X, padx=5, pady=2)
for col in range(9):
    f_menu.columnconfigure(col, weight=1)

SUMMARY_LABELS = [
    "Total Cosmetic Price",
    "Total Grocery Price",
    "Total Cold Drink Price",
]
TAX_LABELS = [
    "Cosmetic Tax (18%)",
    "Grocery Tax (18%)",
    "Cold Drink Tax (18%)",
]

_sum_entries = []
for row, lbl in enumerate(SUMMARY_LABELS):
    Label(f_menu, text=lbl,
          font=("Times New Roman", fs(11), "bold"), bg=BG, fg=FG_WHITE,
          ).grid(row=row, column=0, padx=8, pady=4, sticky="e")
    e = Entry(f_menu, width=12, font=("Times New Roman", fs(11), "bold"),
              bd=6, relief=SUNKEN, justify=RIGHT)
    e.grid(row=row, column=1, padx=5, pady=4, sticky="ew")
    _sum_entries.append(e)
m1_txt, m2_txt, m3_txt = _sum_entries

_tax_entries = []
for row, lbl in enumerate(TAX_LABELS):
    Label(f_menu, text=lbl,
          font=("Times New Roman", fs(11), "bold"), bg=BG, fg=FG_WHITE,
          ).grid(row=row, column=2, padx=8, pady=4, sticky="e")
    e = Entry(f_menu, width=12, font=("Times New Roman", fs(11), "bold"),
              bd=6, relief=SUNKEN, justify=RIGHT)
    e.grid(row=row, column=3, padx=5, pady=4, sticky="ew")
    _tax_entries.append(e)
c1_txt, c2_txt, c3_txt = _tax_entries

btn_frame = Frame(f_menu, bg=BG, relief=GROOVE, bd=6)
btn_frame.grid(row=0, column=4, rowspan=3, columnspan=5,
               padx=10, pady=6, sticky="nsew")
for col in range(4):
    btn_frame.columnconfigure(col, weight=1)
btn_frame.rowconfigure(0, weight=1)

BTN_STYLE = dict(
    font=("Times New Roman", fs(13), "bold"),
    bg="cadetblue", fg="blue", pady=10, bd=4, relief=RAISED,
)
Button(btn_frame, text="Total",         command=refresh_totals, **BTN_STYLE
       ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
Button(btn_frame, text="Generate Bill", command=generate_bill,  **BTN_STYLE
       ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
Button(btn_frame, text="Clear",         command=clear,          **BTN_STYLE
       ).grid(row=0, column=2, padx=10, pady=10, sticky="ew")
Button(btn_frame, text="Exit",          command=win.destroy,    **BTN_STYLE
       ).grid(row=0, column=3, padx=10, pady=10, sticky="ew")

# ── Middle: product panels + bill area ────────────────────────────────────────
mid = Frame(win, bg=BG)
mid.pack(fill=BOTH, expand=True, padx=5, pady=2)
for col in range(4):
    mid.columnconfigure(col, weight=1, uniform="mid_col")
mid.rowconfigure(0, weight=1)

def _build_category_panel(parent, col, heading, category):
    frm = LabelFrame(parent, text=heading, relief=GROOVE,
                     font=("Times New Roman", fs(10), "bold"),
                     fg=FG_GOLD, bg=BG, bd=8)
    frm.grid(row=0, column=col, sticky="nsew", padx=3, pady=3)
    frm.columnconfigure(0, weight=3)
    frm.columnconfigure(1, weight=1)
    for row, (item, price) in enumerate(CATEGORIES[category].items()):
        Label(frm, text=f"{item}  (₹{price})",
              font=("Times New Roman", fs(11), "bold"),
              bg=BG, fg=FG_ITEM, anchor="w",
              ).grid(row=row, column=0, padx=10, pady=7, sticky="w")
        Entry(frm, font=("Times New Roman", fs(11), "bold"),
              textvariable=qty_vars[category][item],
              fg=FG_ENTRY, bd=5, justify=RIGHT, width=6,
              ).grid(row=row, column=1, padx=8, pady=5, sticky="ew")

_build_category_panel(mid, 0, "Cosmetics",   "cosmetics")
_build_category_panel(mid, 1, "Grocery",     "grocery")
_build_category_panel(mid, 2, "Cold Drinks", "cold_drink")

f_bill = Frame(mid, bd=8, relief=GROOVE, bg="white")
f_bill.grid(row=0, column=3, sticky="nsew", padx=3, pady=3)
f_bill.rowconfigure(1, weight=1)
f_bill.columnconfigure(0, weight=1)

Label(f_bill, text="Bill Area",
      font=("Times New Roman", fs(14), "bold"),
      bd=5, relief=GROOVE,
      ).grid(row=0, column=0, columnspan=2, sticky="ew")

v_scroll = Scrollbar(f_bill, orient=VERTICAL)
bill_area = Text(f_bill, yscrollcommand=v_scroll.set,
                 font=("Courier New", fs(10)), wrap=NONE)
v_scroll.config(command=bill_area.yview)
v_scroll.grid(row=1, column=1, sticky="ns")
bill_area.grid(row=1, column=0, sticky="nsew")

win.minsize(900, 550)

win.mainloop()
