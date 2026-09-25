import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.setup_database()
        self.create_widgets()

    def setup_database(self):
        # Set up a SQLite database for storing user BMI data
        self.conn = sqlite3.connect("bmi_data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                date TEXT,
                weight REAL,
                height REAL,
                bmi REAL
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Input fields for weight, height, and name
        ttk.Label(self.root, text="User Name:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = ttk.Entry(self.root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
        self.entry_weight = ttk.Entry(self.root)
        self.entry_weight.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
        self.entry_height = ttk.Entry(self.root)
        self.entry_height.grid(row=2, column=1, padx=10, pady=5)

        # Calculate and view buttons
        ttk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="View Data", command=self.view_data).grid(row=4, column=0, columnspan=2, pady=5)

    def calculate_bmi(self):
        try:
            name = self.entry_name.get()
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if not name or weight <= 0 or height <= 0:
                raise ValueError("Invalid input.")

            bmi = weight / (height ** 2)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute("""
                INSERT INTO bmi_records (user_name, date, weight, height, bmi)
                VALUES (?, ?, ?, ?, ?)
            """, (name, date, weight, height, bmi))
            self.conn.commit()

            messagebox.showinfo("BMI Calculation", f"{name}'s BMI: {bmi:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid weight, height, and name.")

    def view_data(self):
        def display_user_data():
            selected_user = combo_users.get()
            if not selected_user:
                messagebox.showwarning("Selection Error", "Please select a user.")
                return

            self.cursor.execute("SELECT date, bmi FROM bmi_records WHERE user_name = ?", (selected_user,))
            records = self.cursor.fetchall()

            if not records:
                messagebox.showinfo("No Data", f"No data available for user '{selected_user}'.")
                return

            dates, bmi_values = zip(*records)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(dates, bmi_values, marker="o")
            ax.set_title(f"BMI Trend for {selected_user}")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI")
            ax.grid()

            canvas = FigureCanvasTkAgg(fig, master=view_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()
            canvas.draw()

        # Create a new window for data visualization
        view_window = tk.Toplevel(self.root)
        view_window.title("User Data")

        ttk.Label(view_window, text="Select User:").pack(pady=5)
        self.cursor.execute("SELECT DISTINCT user_name FROM bmi_records")
        users = [row[0] for row in self.cursor.fetchall()]
        combo_users = ttk.Combobox(view_window, values=users, state="readonly")
        combo_users.pack(pady=5)

        ttk.Button(view_window, text="Display Data", command=display_user_data).pack(pady=10)

    def close_app(self):
        self.conn.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
