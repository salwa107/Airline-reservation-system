import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import DateEntry

# passengers
flight_prices = {
    '1st Class': {'Adult': 500, 'Child': 350},
    '2nd Class': {'Adult': 300, 'Child': 200},
    '3rd Class': {'Adult': 150, 'Child': 100},
}
#countrise

COUNTRIES = [
    'United States', 'United Kingdom', 'France', 'Germany', 'Japan',
    'Canada', 'Australia', 'India', 'China', 'Brazil', 'Egypt', 'South Africa',
    'Russia', 'Mexico', 'Italy', 'Spain', 'Netherlands', 'Sweden', 'Norway',
]

bookings = []  
#بجمع الحجوزات لان مفيش تسجيل دخول 
def calculate_price(adults, children, grade):
    return adults * flight_prices[grade]['Adult'] + children * flight_prices[grade]['Child']

class AirlineApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Airline Booking System")
        self.root.geometry("450x600")
        self.show_home()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to Airline Booking", font=('Arial', 18)).pack(pady=15)

        tk.Button(self.root, text="Book a Flight", width=25, command=self.show_booking).pack(pady=8)
        tk.Button(self.root, text="Change Booking", width=25, command=self.show_change_booking).pack(pady=8)
        tk.Button(self.root, text="Booking History", width=25, command=self.show_history).pack(pady=8)

    def show_booking(self):
        self.clear_frame()
        tk.Label(self.root, text="Book a Flight", font=('Arial', 16)).pack(pady=10)

        tk.Label(self.root, text="Trip Type").pack()
        self.trip_type = tk.StringVar(value="One Way")
        ttk.Combobox(self.root, values=["One Way", "Round Trip", "Multi-City"], textvariable=self.trip_type, state="readonly").pack()

        tk.Label(self.root, text="From Country").pack()
        self.from_country = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.from_country, values=COUNTRIES, state="readonly").pack()

        tk.Label(self.root, text="To Country").pack()
        self.to_country = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.to_country, values=COUNTRIES, state="readonly").pack()

        tk.Label(self.root, text="Date").pack()
        self.date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.date_entry.pack()

        tk.Label(self.root, text="Hour").pack()
        self.hour_var = tk.StringVar(value="00")
        ttk.Combobox(self.root, textvariable=self.hour_var, values=[f"{h:02}" for h in range(24)], state="readonly").pack()

        tk.Label(self.root, text="Minute").pack()
        self.minute_var = tk.StringVar(value="00")
        ttk.Combobox(self.root, textvariable=self.minute_var, values=[f"{m:02}" for m in range(0, 60, 5)], state="readonly").pack()

        tk.Label(self.root, text="Adults").pack()
        self.adults_var = tk.IntVar(value=1)
        tk.Spinbox(self.root, from_=0, to=10, textvariable=self.adults_var).pack()

        tk.Label(self.root, text="Children").pack()
        self.children_var = tk.IntVar(value=0)
        tk.Spinbox(self.root, from_=0, to=10, textvariable=self.children_var).pack()

        tk.Label(self.root, text="Class").pack()
        self.grade_var = tk.StringVar(value='3rd Class')
        ttk.Combobox(self.root, values=list(flight_prices.keys()), textvariable=self.grade_var, state="readonly").pack()

        self.price_label = tk.Label(self.root, text="Price: $0", font=('Arial', 12))
        self.price_label.pack(pady=5)

        self.adults_var.trace_add("write", self.update_price)
        self.children_var.trace_add("write", self.update_price)
        self.grade_var.trace_add("write", self.update_price)

        tk.Button(self.root, text="Confirm Booking", command=self.confirm_booking).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_home).pack()

        self.update_price()

    def update_price(self, *args):
        adults = self.adults_var.get()
        children = self.children_var.get()
        grade = self.grade_var.get()
        price = calculate_price(adults, children, grade)
        self.price_label.config(text=f"Price: ${price}")

    def confirm_booking(self):
        from_c = self.from_country.get()
        to_c = self.to_country.get()
        if from_c == "" or to_c == "":
            messagebox.showerror("Error", "Please select both From and To countries")
            return
        if from_c == to_c:
            messagebox.showerror("Error", "From and To countries cannot be the same")
            return

        selected_date = self.date_entry.get()
        selected_hour = self.hour_var.get()
        selected_minute = self.minute_var.get()
        full_datetime = f"{selected_date} {selected_hour}:{selected_minute}"

        try:
            flight_date = datetime.strptime(full_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date and time")
            return

        adults = self.adults_var.get()
        children = self.children_var.get()
        grade = self.grade_var.get()
        trip_type = self.trip_type.get()
        price = calculate_price(adults, children, grade)

        booking = {
            'trip_type': trip_type,
            'from': from_c,
            'to': to_c,
            'date': flight_date,
            'adults': adults,
            'children': children,
            'class': grade,
            'price': price,
        }

        bookings.append(booking)
        messagebox.showinfo("Booked", "Flight booked successfully!")
        self.show_home()

    def show_history(self):
        self.clear_frame()
        tk.Label(self.root, text="Booking History", font=('Arial', 16)).pack(pady=10)

        if not bookings:
            tk.Label(self.root, text="No bookings found").pack(pady=10)
        else:
            now = datetime.now()
            for i, b in enumerate(bookings):
                time_left = b['date'] - now
                remaining = str(time_left).split('.')[0] if time_left.total_seconds() > 0 else "Departed"
                details = (
                    f"{b['trip_type']} | {b['from']} → {b['to']} | "
                    f"{b['date'].strftime('%Y-%m-%d %H:%M')} | Class: {b['class']} | "
                    f"Adults: {b['adults']} Children: {b['children']} | "
                    f"Total: ${b['price']} | Time Left: {remaining}"
                )
                tk.Label(self.root, text=details, wraplength=400, justify="left").pack(anchor='w', padx=10, pady=3)

        tk.Button(self.root, text="Back", command=self.show_home).pack(pady=15)

    def show_change_booking(self):
        self.clear_frame()
        tk.Label(self.root, text="Change Booking", font=('Arial', 16)).pack(pady=10)

        if not bookings:
            tk.Label(self.root, text="No bookings to change").pack(pady=10)
            tk.Button(self.root, text="Back", command=self.show_home).pack()
            return

        self.selected_booking = tk.StringVar()
        options = [f"{b['from']} to {b['to']} on {b['date'].strftime('%Y-%m-%d %H:%M')}" for b in bookings]
        dropdown = ttk.Combobox(self.root, values=options, textvariable=self.selected_booking, state="readonly")
        dropdown.pack()

        def load_booking():
            if self.selected_booking.get() not in options:
                messagebox.showerror("Error", "Please select a booking")
                return
            idx = options.index(self.selected_booking.get())
            self.edit_booking(bookings[idx])

        tk.Button(self.root, text="Edit Selected Booking", command=load_booking).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_home).pack()

    def edit_booking(self, booking):
        self.clear_frame()
        tk.Label(self.root, text="Edit Booking", font=('Arial', 16)).pack(pady=10)

        tk.Label(self.root, text="From Country").pack()
        from_entry = ttk.Combobox(self.root, values=COUNTRIES, state="readonly")
        from_entry.set(booking['from'])
        from_entry.pack()

        tk.Label(self.root, text="To Country").pack()
        to_entry = ttk.Combobox(self.root, values=COUNTRIES, state="readonly")
        to_entry.set(booking['to'])
        to_entry.pack()

        tk.Label(self.root, text="Date").pack()
        date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        date_entry.set_date(booking['date'])
        date_entry.pack()

        tk.Label(self.root, text="Hour").pack()
        hour_var = tk.StringVar(value=booking['date'].strftime("%H"))
        hour_combo = ttk.Combobox(self.root, values=[f"{h:02}" for h in range(24)], textvariable=hour_var, state="readonly")
        hour_combo.pack()

        tk.Label(self.root, text="Minute").pack()
        minute_var = tk.StringVar(value=booking['date'].strftime("%M"))
        minute_combo = ttk.Combobox(self.root, values=[f"{m:02}" for m in range(0, 60, 5)], textvariable=minute_var, state="readonly")
        minute_combo.pack()

        tk.Label(self.root, text="Adults").pack()
        adults_var = tk.IntVar(value=booking['adults'])
        tk.Spinbox(self.root, from_=0, to=10, textvariable=adults_var).pack()

        tk.Label(self.root, text="Children").pack()
        children_var = tk.IntVar(value=booking['children'])
        tk.Spinbox(self.root, from_=0, to=10, textvariable=children_var).pack()

        tk.Label(self.root, text="Class").pack()
        grade_var = tk.StringVar(value=booking['class'])
        grade_combo = ttk.Combobox(self.root, values=list(flight_prices.keys()), textvariable=grade_var, state="readonly")
        grade_combo.pack()

        price_label = tk.Label(self.root, text="", font=('Arial', 12))
        price_label.pack(pady=5)

        def update_price(*args):
            price = calculate_price(adults_var.get(), children_var.get(), grade_var.get())
            price_label.config(text=f"Price: ${price}")

        adults_var.trace_add("write", update_price)
        children_var.trace_add("write", update_price)
        grade_var.trace_add("write", update_price)
        update_price()

        def save_changes():
            from_c = from_entry.get()
            to_c = to_entry.get()
            if from_c == "" or to_c == "":
                messagebox.showerror("Error", "Please select both From and To countries")
                return
            if from_c == to_c:
                messagebox.showerror("Error", "From and To countries cannot be the same")
                return

            date_str = date_entry.get()
            h = hour_var.get()
            m = minute_var.get()
            try:
                new_date = datetime.strptime(f"{date_str} {h}:{m}", "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date and time")
                return

            booking['from'] = from_c
            booking['to'] = to_c
            booking['date'] = new_date
            booking['adults'] = adults_var.get()
            booking['children'] = children_var.get()
            booking['class'] = grade_var.get()
            booking['price'] = calculate_price(adults_var.get(), children_var.get(), grade_var.get())

            messagebox.showinfo("Saved", "Booking updated successfully!")
            self.show_home()

        tk.Button(self.root, text="Save Changes", command=save_changes).pack(pady=10)
        tk.Button(self.root, text="Cancel", command=self.show_home).pack()

if _name_ == "_main_":
    root = tk.Tk()
    app = AirlineApp(root)
    root.mainloop()
