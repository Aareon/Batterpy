import tkinter as tk
from tkinter import ttk, messagebox
from batterpy.report_generator import generate_battery_report, parse_xml, get_report_information, get_system_information, get_battery_information, get_recent_usage
from batterpy.calculations import calculate_battery_health, calculate_battery_degradation
from batterpy.display_functions import display_report_information, display_system_information, display_battery_information, display_recent_usage
from batterpy.graph_generator import create_graphs, update_graphs
from loguru import logger

def generate_and_display_report():
    report_path = generate_battery_report()
    root = parse_xml(report_path)
    if root is None:
        messagebox.showerror("Error", "Failed to parse the battery report.")
        return
    
    ns = '{http://schemas.microsoft.com/battery/2012}'
    
    report_info = get_report_information(root, ns)
    system_info = get_system_information(root, ns)
    battery_info = get_battery_information(root, ns)
    recent_usage = get_recent_usage(root, ns)
    
    display_report_information(report_info)
    display_system_information(system_info)
    display_battery_information(battery_info, calculate_battery_health, calculate_battery_degradation)
    display_recent_usage(recent_usage)
    
    report_text.config(state=tk.NORMAL)
    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, format_dict(report_info))
    report_text.config(state=tk.DISABLED)
    
    system_text.config(state=tk.NORMAL)
    system_text.delete(1.0, tk.END)
    system_text.insert(tk.END, format_dict(system_info))
    system_text.config(state=tk.DISABLED)
    
    battery_text.config(state=tk.NORMAL)
    battery_text.delete(1.0, tk.END)
    battery_text.insert(tk.END, "\n\n".join([format_dict(battery) + f"\nHealth: {calculate_battery_health(battery):.2f}%\nDegradation: {calculate_battery_degradation(battery):.2f}%" for battery in battery_info]))
    battery_text.config(state=tk.DISABLED)
    
    # Update Treeview with recent usage
    for i in usage_tree.get_children():
        usage_tree.delete(i)
    for usage in recent_usage:
        usage_tree.insert("", "end", values=list(usage.values()))
    
    # Update graphs
    update_graphs(fig1, canvas1, fig2, canvas2, fig3, canvas3, fig4, canvas4, fig5, canvas5, fig6, canvas6, fig7, canvas7, fig8, canvas8, fig9, canvas9, recent_usage, battery_info)

def format_dict(data):
    return "\n".join([f"{key}: {value}" for key, value in data.items()])

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

app = tk.Tk()
app.title("Battery Report Viewer")

# Create style
style = ttk.Style()
style.configure('TLabel', padding=5, font=('Helvetica', 12))
style.configure('TButton', padding=5, font=('Helvetica', 12))
style.configure('TNotebook', font=('Helvetica', 12))
style.configure('TNotebook.Tab', padding=10, font=('Helvetica', 12))

# Create Notebook for tabs
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True)

# Create frames for tabs
frame_report = ttk.Frame(notebook, padding="10 10 10 10")
frame_system = ttk.Frame(notebook, padding="10 10 10 10")
frame_battery = ttk.Frame(notebook, padding="10 10 10 10")
frame_usage = ttk.Frame(notebook, padding="10 10 10 10")

# Create a canvas and a scrollbar for the graphs
frame_graphs_container = ttk.Frame(notebook)
canvas = tk.Canvas(frame_graphs_container)
scroll_y = tk.Scrollbar(frame_graphs_container, orient="vertical", command=canvas.yview)
frame_graphs = ttk.Frame(canvas)

# Add frames to notebook
notebook.add(frame_report, text='Report Information')
notebook.add(frame_system, text='System Information')
notebook.add(frame_battery, text='Battery Information')
notebook.add(frame_usage, text='Recent Usage')
notebook.add(frame_graphs_container, text='Graphs')

# Configure canvas and scrollbar
canvas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=frame_graphs, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_graphs.bind("<Configure>", on_frame_configure)
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Report Information
ttk.Label(frame_report, text="Report Information", style='TLabel').pack(anchor=tk.W)
report_text = tk.Text(frame_report, wrap='word', height=10, state=tk.DISABLED, font=('Helvetica', 10))
report_text.pack(fill='both', expand=True)

# System Information
ttk.Label(frame_system, text="System Information", style='TLabel').pack(anchor=tk.W)
system_text = tk.Text(frame_system, wrap='word', height=10, state=tk.DISABLED, font=('Helvetica', 10))
system_text.pack(fill='both', expand=True)

# Battery Information
ttk.Label(frame_battery, text="Battery Information", style='TLabel').pack(anchor=tk.W)
battery_text = tk.Text(frame_battery, wrap='word', height=10, state=tk.DISABLED, font=('Helvetica', 10))
battery_text.pack(fill='both', expand=True)

# Recent Usage
ttk.Label(frame_usage, text="Recent Usage", style='TLabel').pack(anchor=tk.W)

# Create Treeview for recent usage
columns = ("Timestamp", "LocalTimestamp", "Duration", "Ac", "EntryType", "ChargeCapacity", "Discharge", "FullChargeCapacity", "IsNextOnBattery")
usage_tree = ttk.Treeview(frame_usage, columns=columns, show="headings", height=10)
for col in columns:
    usage_tree.heading(col, text=col)
    usage_tree.column(col, width=100)

# Add Treeview to frame with a scrollbar
scrollbar = ttk.Scrollbar(frame_usage, orient=tk.VERTICAL, command=usage_tree.yview)
usage_tree.configure(yscroll=scrollbar.set)
usage_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Graphs
fig1, canvas1, fig2, canvas2, fig3, canvas3, fig4, canvas4, fig5, canvas5, fig6, canvas6, fig7, canvas7, fig8, canvas8, fig9, canvas9, _ = create_graphs(frame_graphs)

# Generate Report Button
ttk.Button(app, text="Generate Report", command=generate_and_display_report, style='TButton').pack(pady=10)

logger.add("battery_report.log", rotation="1 MB")
app.mainloop()
