import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Main Application Window
root = Tk()
root.title("Bus Ticket Booking System")
root.geometry("800x660")
root.configure(bg="#dff5ff")  # Light blue background

# Header
header = Label(root, text="🚌 BUS TICKET BOOKING SYSTEM 🚌", font=("Arial", 20, "bold"), bg="#87cefa", fg="white")
header.pack(fill=X)

# Form Frame
form_frame = Frame(root, bg="#f0f8ff", bd=5, relief=RIDGE)
form_frame.place(x=50, y=80, width=700, height=400)

# Input Fields
fields = ["Name", "Depart Date", "Return Date", "Origin", "Destination"]
entries = {}

for idx, field in enumerate(fields):
    label = Label(form_frame, text=f"{field}:", font=("Arial", 12), bg="#f0f8ff", anchor="w")
    label.grid(row=idx, column=0, pady=5, padx=10, sticky="w")

    entry = Entry(form_frame, font=("Arial", 12), bg="white", fg="black", bd=2)
    entry.grid(row=idx, column=1, pady=5, padx=10, sticky="w")
    entries[field] = entry

bus_type_options = ["AC", "Non-AC"]
bus_type_var = StringVar()
bus_type_var.set(bus_type_options[0])
Label(form_frame, text="Bus Type:", font=("Arial", 12), bg="#f0f8ff").grid(row=5, column=0, pady=5, padx=10, sticky="w")
bus_type_menu = OptionMenu(form_frame, bus_type_var, *bus_type_options)
bus_type_menu.grid(row=5, column=1, pady=5, padx=10, sticky="w")

# Dropdown for Travel Time
travel_time_options = ["00:00 AM - 11:59 AM", "12:00 PM - 06:59 PM", "07:00 PM - 11:59 PM"]
travel_time_var = StringVar()
travel_time_var.set(travel_time_options[0])
Label(form_frame, text="Travel Time:", font=("Arial", 12), bg="#f0f8ff").grid(row=6, column=0, pady=5, padx=10, sticky="w")
travel_time_menu = OptionMenu(form_frame, travel_time_var, *travel_time_options)
travel_time_menu.grid(row=6, column=1, pady=5, padx=10, sticky="w")

# Functions
def book_ticket():
    name = entries["Name"].get()
    depart_date = entries["Depart Date"].get()
    return_date = entries["Return Date"].get()
    origin = entries["Origin"].get()
    destination = entries["Destination"].get()
    travel_time = travel_time_var.get()

    if not all([name, depart_date, return_date, origin, destination]):
        messagebox.showerror("Error", "All fields are required")
    else:
        with open("bookings.txt", "a") as file:
            file.write(f"{name}, {depart_date}, {return_date}, {origin}, {destination}, {bus_type_var.get()}, {travel_time}\n")
        messagebox.showinfo("Success", "Ticket booked successfully!")

def cancel_ticket():
    name = entries["Name"].get()
    if not name:
        messagebox.showerror("Error", "Name is required to cancel ticket")
        return

    with open("bookings.txt", "r") as file:
        lines = file.readlines()

    with open("bookings.txt", "w") as file:
        for line in lines:
            if name not in line:
                file.write(line)
    messagebox.showinfo("Success", "Ticket canceled successfully!")

def display_bookings():
    with open("bookings.txt", "r") as file:
        bookings = file.read()
    if not bookings.strip():
        messagebox.showinfo("Bookings", "No bookings found.")
    else:
        messagebox.showinfo("Bookings", bookings)

def check_availability():
    with open("bookings.txt", "r") as file:
        num_entries = len(file.readlines())
    num_available = 50 - num_entries
    messagebox.showinfo("Availability", f"{num_available} seats available")

def list_buses():
    buses_window = Toplevel(root)
    buses_window.title("Buses Available")
    buses_window.geometry("600x400")
    
    # Retrieve selected travel time
    selected_travel_time = travel_time_var.get()

    # Simulated data for available buses
    buses = [
        {"company": "Super Nice", "departure": "09:45 AM", "price": "RM 55.00", "rating": "4.2", "seats": "38", "reschedulable": True, "refundable": True, "code": "SVIP27TB"},
        {"company": "Plusliner", "departure": "11:30 AM", "price": "RM 50.00", "rating": "4.7", "seats": "30", "reschedulable": False, "refundable": True, "code": "PL1234"},
        {"company": "Super Nice", "departure": "12:45 PM", "price": "RM 45.00", "rating": "4.3", "seats": "26", "reschedulable": True, "refundable": True, "code": "SVIP27TB"},
        {"company": "Transnasional", "departure": "01:15 PM", "price": "RM 47.00", "rating": "4.0", "seats": "30", "reschedulable": False, "refundable": False, "code": "TN5678"}
    ]

    # Add title
    Label(buses_window, text="AVAILABLE BUSES", font=("Algerian", 20), bg="light blue").pack(fill=X, pady=10)

    # Filter buses based on selected travel time
    for bus in buses:
        departure = bus['departure']
        hour = int(departure.split(":")[0])
        meridian = departure.split(" ")[1]

        # Filter by selected time range
        if (selected_travel_time == "00:00 AM - 11:59 AM" and meridian == "AM") or \
           (selected_travel_time == "12:00 PM - 06:59 PM" and meridian == "PM" and hour < 7) or \
           (selected_travel_time == "07:00 PM - 11:59 PM" and meridian == "PM" and hour >= 7):

            # Format bus information
            bus_info = f"Company: {bus['company']}\n"
            bus_info += f"Departure: {bus['departure']}\n"
            bus_info += f"Price: {bus['price']}\n"
            if bus['rating']:
                bus_info += f"Rating: {bus['rating']} stars\n"
            bus_info += f"Seats Available: {bus['seats']}\n"
            if bus['reschedulable']:
                bus_info += "Reschedulable\n"
            if bus['refundable']:
                bus_info += "Refundable\n"
            if bus['code']:
                bus_info += f"Bus Code: {bus['code']}\n"

            # Display each bus as a Label
            Label(buses_window, text=bus_info, font=("Times New Roman", 12), bg="white", justify=LEFT, anchor="w", relief=SOLID, bd=1).pack(fill="x", padx=10, pady=5)

# Buttons
btn_frame = Frame(root, bg="#dff5ff")
btn_frame.place(x=30, y=500, width=800)

buttons = [
    ("Book Ticket", book_ticket),
    ("Cancel Ticket", cancel_ticket),
    ("Display Bookings", display_bookings),
    ("Check Availability", check_availability),
    ("Buses Available", list_buses)
]

# Dynamically organize buttons into rows of 3
for idx, (btn_text, btn_command) in enumerate(buttons):
    btn = Button(btn_frame, text=btn_text, command=btn_command, font=("Arial", 12, "bold"),
                 bg="#00bfff", fg="white", padx=10, pady=5, width=20)
    btn.grid(row=idx // 3, column=idx % 3, padx=10, pady=5)


# Footer
footer = Label(root, text="Powered by Python & Tkinter", font=("Arial", 10), bg="#87cefa", fg="white")
footer.pack(side=BOTTOM, fill=X)

root.mainloop()
