import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Function to add an expense
def add_expense():
    date = date_entry.get()
    date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    description = description_entry.get()
    category = category_entry.get()
    price = price_entry.get()

    cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                (date, description, category, price))
    conn.commit()
    messagebox.showinfo("Info", "Expense added successfully!")

# Function to view all expenses
def view_all_expenses():
    view_window = tk.Toplevel(root)
    view_window.title("View All Expenses")
    view_window.geometry("800x600")

    frame = ttk.Frame(view_window, padding="10")
    frame.place(relwidth=1, relheight=1)
    frame.configure(style="Custom.TFrame")

    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    for expense in expenses:
        ttk.Label(frame, text=f"Date: {expense[1]}, Description: {expense[2]}, Category: {expense[3]}, Price: {expense[4]}",
                  font=("Arial", 14)).pack(pady=5)

# Function to view monthly expenses by category
def view_monthly_expenses():
    view_window = tk.Toplevel(root)
    view_window.title("View Monthly Expenses by Category")
    view_window.geometry("800x600")

    frame = ttk.Frame(view_window, padding="10")
    frame.place(relwidth=1, relheight=1)
    frame.configure(style="Custom.TFrame")

    month = month_entry.get()
    year = year_entry.get()
    cur.execute("""SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                   GROUP BY category""", (month, year))
    expenses = cur.fetchall()
    for expense in expenses:
        ttk.Label(frame, text=f"Category: {expense[0]}, Total: {expense[1]}",
                  font=("Arial", 14)).pack(pady=5)

# Function to delete expenses
def delete_expenses():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Expenses")

    def delete_by_date():
        date = date_entry.get()
        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        cur.execute("DELETE FROM expenses WHERE Date = ?", (date,))
        conn.commit()
        messagebox.showinfo("Info", f"Records for {date} deleted.")
        delete_window.destroy()

    def delete_by_range():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        cur.execute("DELETE FROM expenses WHERE Date BETWEEN ? AND ?", (start_date, end_date))
        conn.commit()
        messagebox.showinfo("Info", f"Records from {start_date} to {end_date} deleted.")
        delete_window.destroy()

    def delete_all():
        cur.execute("DELETE FROM expenses")
        conn.commit()
        messagebox.showinfo("Info", "All records deleted.")
        delete_window.destroy()

    ttk.Label(delete_window, text="Delete by specific date (DD-MM-YYYY):", font=("Arial", 12)).pack(pady=5)
    date_entry = ttk.Entry(delete_window, font=("Arial", 12))
    date_entry.pack(pady=5)
    ttk.Button(delete_window, text="Delete", command=delete_by_date, style="TButton").pack(pady=5)

    ttk.Label(delete_window, text="Delete by date range (DD-MM-YYYY):", font=("Arial", 12)).pack(pady=5)
    start_date_entry = ttk.Entry(delete_window, font=("Arial", 12))
    start_date_entry.pack(pady=5)
    end_date_entry = ttk.Entry(delete_window, font=("Arial", 12))
    end_date_entry.pack(pady=5)
    ttk.Button(delete_window, text="Delete", command=delete_by_range, style="TButton").pack(pady=5)

    ttk.Label(delete_window, text="Delete all expenses:", font=("Arial", 12)).pack(pady=5)
    ttk.Button(delete_window, text="Delete All", command=delete_all, style="TButton").pack(pady=5)

# Database connection
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Ensure tables exist
cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()

# Tkinter UI
root = tk.Tk()
root.title("Expense Tracker")

# Set theme
style = ttk.Style(root)
style.theme_use('clam')

# Define custom styles
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("Custom.TFrame", background="#D3D3D3")  # Light grey background

# Background image
image_path = "C:/Users/Amaya/Downloads/WhatsApp Image 2024-11-06 at 23.14.41_019eb60a.jpg"
background_image = Image.open(image_path)
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Frame for content
frame = ttk.Frame(root, padding="10")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add Title Text
ttk.Label(frame, text="Expense Tracker", font=("Arial", 24, "bold")).grid(row=0, columnspan=2, pady=10)

# Add Expense
ttk.Label(frame, text="Add Expense", font=("Arial", 18, "bold")).grid(row=1, columnspan=2, pady=10)
ttk.Label(frame, text="Date (DD-MM-YYYY):", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
date_entry = ttk.Entry(frame, font=("Arial", 14))
date_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(frame, text="Description:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
description_entry = ttk.Entry(frame, font=("Arial", 14))
description_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(frame, text="Category:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
category_entry = ttk.Entry(frame, font=("Arial", 14))
category_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(frame, text="Price:", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
price_entry = ttk.Entry(frame, font=("Arial", 14))
price_entry.grid(row=5, column=1, padx=10, pady=5)

ttk.Button(frame, text="Add Expense", command=add_expense).grid(row=6, columnspan=2, pady=10)

# View Buttons
ttk.Button(frame, text="View All Expenses", command=view_all_expenses).grid(row=7, column=0, padx=10, pady=5)
ttk.Button(frame, text="Delete Expenses", command=delete_expenses).grid(row=7, column=1, padx=10, pady=5)

# Entry fields for month and year
ttk.Label(frame, text="Month (MM):", font=("Arial", 14)).grid(row=8, column=0, padx=10, pady=5, sticky=tk.E)
month_entry = ttk.Entry(frame, font=("Arial", 14))
month_entry.grid(row=8, column=1, padx=10, pady=5)

ttk.Label(frame, text="Year (YYYY):", font=("Arial", 14)).grid(row=9, column=0, padx=10, pady=5, sticky=tk.E)
year_entry = ttk.Entry(frame, font=("Arial", 14))
year_entry.grid(row=9, column=1, padx=10, pady=5)

# Monthly Expenses Button
ttk.Button(frame, text="View Monthly Expenses by Category", command=view_monthly_expenses).grid(row=10, columnspan=2, pady=5)

# Make the window fill the screen
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.mainloop()

# Close database connection
conn.close()


