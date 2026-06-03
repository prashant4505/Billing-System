# Billing System

A desktop billing application built with Python and Tkinter. Supports cosmetics, grocery, and cold drink categories with automatic tax calculation, bill generation, and bill saving/searching.

---

## Requirements

- Python 3.6 or higher
- `tkinter` (included with Python on Windows and macOS)

### Linux — install tkinter if missing

| Distro | Command |
|---|---|
| Ubuntu / Debian | `sudo apt-get install python3-tk` |
| Fedora / RHEL | `sudo dnf install python3-tkinter` |
| Arch Linux | `sudo pacman -S tk` |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Billing-System.git
cd Billing-System
```

### 2. (Optional) Create a virtual environment

```bash
python3 -m venv venv

# Activate — Linux / macOS
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install dependencies

No third-party packages are required. All modules (`tkinter`, `random`, `os`) are part of the Python standard library.

```bash
pip install -r requirements.txt   # reads the file; nothing to download
```

### 4. Run the application

```bash
# Linux / macOS
python3 main.py

# Windows
python main.py
```

The window opens maximised and scales automatically to your screen size.

---

## How to Use

| Step | Action |
|---|---|
| 1 | Enter **Customer Name**, **Contact No** in the top bar |
| 2 | Type quantities for any products across the three category panels |
| 3 | Click **Total** to calculate subtotals and taxes |
| 4 | Click **Generate Bill** to preview the bill and optionally save it |
| 5 | To find a saved bill, type its number in **Bill No** and click **Search** |
| 6 | Click **Clear** to reset the form for the next customer |

---

## Project Structure

```
Billing-System/
├── main.py            # Application entry point
├── requirements.txt   # Dependency notes
├── README.md          # This file
├── bills/             # Saved bills (auto-created on first save)
│   └── <bill_no>.txt
└── icon/
    └── rubik_cube_icon_182136.ico
```

---

## Features

- Responsive UI — fits any screen size automatically
- Three product categories: Cosmetics, Grocery, Cold Drinks
- 18% GST calculated per category
- Random bill number generated per transaction
- Bills saved as `.txt` files and searchable by bill number
