import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import os
import math

#Classes
class TrackEvent:
    def __init__(self, name):
        self.name = name
        self.results = []
    def add_result(self, value):
        self.results.append(value)
    def get_best(self):
        return min(self.results) if self.results else None #returns lowest time

class FieldEvent(TrackEvent):
    def get_best(self):
        return max(self.results) if self.results else None #returns highest mark

#IAAF Scoring
iaaf_all_events = {
    #Track Events
    "100m": {"A": 25.4347, "B": 18.0, "C": 1.81, "type": "track"},
    "200m": {"A": 5.8425, "B": 38.0, "C": 1.81, "type": "track"},
    "400m": {"A": 1.53775, "B": 82.0, "C": 1.81, "type": "track"},
    "800m": {"A": 0.13279, "B": 345.0, "C": 1.85, "type": "track"},
    "1500m": {"A": 0.03768, "B": 480.0, "C": 1.85, "type": "track"},
    "5000m": {"A": 0.00914, "B": 1250.0, "C": 1.85, "type": "track"},
    "10000m": {"A": 0.00213, "B": 3050.0, "C": 1.85, "type": "track"},
    "110mH": {"A": 5.74352, "B": 28.5, "C": 1.92, "type": "track"},
    "400mH": {"A": 1.13757, "B": 92.0, "C": 1.81, "type": "track"},
    "3000mSC": {"A": 0.092, "B": 600.0, "C": 1.85, "type": "track"},

    #Field Events
    "LongJump": {"A": 0.14354, "B": 220.0, "C": 1.4, "type": "field", "to_cm": True},
    "TripleJump": {"A": 0.188807, "B": 210.0, "C": 1.41, "type": "field", "to_cm": True},
    "HighJump": {"A": 0.8465, "B": 75.0, "C": 1.42, "type": "field", "to_cm": True},
    "PoleVault": {"A": 0.2797, "B": 100.0, "C": 1.35, "type": "field", "to_cm": True},
    "ShotPut": {"A": 51.39, "B": 1.5, "C": 1.05, "type": "field"},
    "Discus": {"A": 12.91, "B": 4.0, "C": 1.1, "type": "field"},
    "Javelin": {"A": 10.14, "B": 7.0, "C": 1.08, "type": "field"},
    "Hammer": {"A": 13.407, "B": 7.0, "C": 1.05, "type": "field"},
    
    #Multi
    "Decathlon": {"custom": True},
    "Heptathlon": {"custom": True},
}

def calc_iaaf_points(event, performance):
    if event not in iaaf_all_events:
        raise ValueError(f"No scoring data for {event}")
    data = iaaf_all_events[event]
    if data.get("custom"):
        return 0
    A, B, C = data['A'], data['B'], data['C']
    P = performance * 100 if data.get("to_cm") else performance
    try:
        if data['type'] == 'track':
            return int(A*((B-P)**C))
        elif data['type'] == 'field':
            return int(A*((P-B)**C))
    except:
        return 0

results = {}

#Saving/Loading Results
def save_results(events):
    with open("results.txt", 'w') as file:
        for event_name, event_obj in events.items():
            file.write(f"{event_name}:{','.join(map(str, event_obj.results))}\n")

def load_results():
    events = {
        "100m": TrackEvent("100m"),
        "400m": TrackEvent("400m"),
        "LongJump": FieldEvent("LongJump"),
        "HighJump": FieldEvent("HighJump")
        }
    if os.path.exists("results.txt"):
               with open("results.txt", "r") as file:
                   for line in file:
                       name, data = line.strip().split(":")
                       values = list(map(float, data.split(",")))
                       for v in values:
                           events[name].add_result(v)
    return events

results = load_results()

#Add new event in case missing
def get_event_object(event_name):
    if event_name not in results:
        if iaaf_all_events[event_name]['type'] == 'track':
            results[event_name] = TrackEvent(event_name)
        else:
            results[event_name] = FieldEvent(event_name)
    return results[event_name]

#Submitting results
def submit_result():
    event = event_entry.get()
    try:
        value = float(result_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for result")
        return
    if event not in iaaf_all_events:
        messagebox.showerror("Error", "Invalid event name")
        return
    event_obj = get_event_object(event)
    event_obj.add_result(value)
    messagebox.showinfo("Success", f"Result {value} added to {event}")
  
#Show personal bests and points
def show_summary():
    summary = ''
    total_points = 0
    for event, obj in results.items():
        best = obj.get_best()
        if best is not None:
            points = calc_iaaf_points(event, best)
            total_points +=points
            summary += f"{event} - Best: {best}, Points: {points}\n"
    summary+= f"Total Points: {total_points}"
    messagebox.showinfo("Performance Summary:", summary)

#Plot performance progression
def plot_progress():
    event = event_entry.get()
    if event not in results:
        messagebox.showerror("Error", "No data for this event")
        return
    data = results[event].results
    if not data:
        messagebox.showinfo("No data", f"No results available for {event}")
        return
    plt.figure()
    plt.plot(range(1, len(data) + 1), data, marker='o')
    plt.title(f"{event} Performance Progression")
    plt.xlabel("Attempt")
    plt.ylabel("Time/Mark")
    plt.grid(True)
    plt.show()

#Saving before exit
def on_exit():
    save_results(results)
    root.destroy()

#GUI
root = tk.Tk()
root.title("Track and Field Performance Tracker")

tk.Label(root, text='Event:').grid(row=0, column=0, padx=10, pady=5)
event_entry = tk.Entry(root)
event_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text='Result:').grid(row=1, column=0, padx=10, pady=5)
result_entry = tk.Entry(root)
result_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text='Add Result', command=submit_result).grid(row=2, column=0, pady=10)
tk.Button(root, text='Show Summary', command=show_summary).grid(row=2, column=1)
tk.Button(root, text='Plot Progress', command=plot_progress).grid(row=3, column=0, columnspan=2)
tk.Button(root, text='Exit', command=on_exit).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

        