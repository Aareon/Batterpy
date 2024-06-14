import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .calculations import (calculate_battery_health, calculate_historical_health, calculate_cycle_count_over_time,
                          calculate_discharge_rate, calculate_average_discharge_rate, count_charge_discharge_cycles, 
                          estimate_time_to_full_charge, estimate_time_to_empty, calculate_energy_consumption)
import tkinter as tk
from typing import List, Dict

def create_graphs(parent_frame):
    frame = tk.Frame(parent_frame)
    frame.pack(fill=tk.BOTH, expand=True)

    fig1 = Figure(figsize=(8, 6), dpi=100)
    canvas1 = FigureCanvasTkAgg(fig1, master=frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig2 = Figure(figsize=(8, 6), dpi=100)
    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig3 = Figure(figsize=(8, 6), dpi=100)
    canvas3 = FigureCanvasTkAgg(fig3, master=frame)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig4 = Figure(figsize=(8, 6), dpi=100)
    canvas4 = FigureCanvasTkAgg(fig4, master=frame)
    canvas4.draw()
    canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig5 = Figure(figsize=(8, 6), dpi=100)
    canvas5 = FigureCanvasTkAgg(fig5, master=frame)
    canvas5.draw()
    canvas5.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig6 = Figure(figsize=(8, 6), dpi=100)
    canvas6 = FigureCanvasTkAgg(fig6, master=frame)
    canvas6.draw()
    canvas6.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig7 = Figure(figsize=(8, 6), dpi=100)
    canvas7 = FigureCanvasTkAgg(fig7, master=frame)
    canvas7.draw()
    canvas7.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig8 = Figure(figsize=(8, 6), dpi=100)
    canvas8 = FigureCanvasTkAgg(fig8, master=frame)
    canvas8.draw()
    canvas8.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig9 = Figure(figsize=(8, 6), dpi=100)
    canvas9 = FigureCanvasTkAgg(fig9, master=frame)
    canvas9.draw()
    canvas9.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    return fig1, canvas1, fig2, canvas2, fig3, canvas3, fig4, canvas4, fig5, canvas5, fig6, canvas6, fig7, canvas7, fig8, canvas8, fig9, canvas9, frame

def update_graphs(fig1, canvas1, fig2, canvas2, fig3, canvas3, fig4, canvas4, fig5, canvas5, fig6, canvas6, fig7, canvas7, fig8, canvas8, fig9, canvas9, recent_usage: List[Dict[str, str]], battery_info: List[Dict[str, str]]):
    timestamps = [entry['Timestamp'] for entry in recent_usage]
    charge_capacities = [int(entry['ChargeCapacity']) for entry in recent_usage]
    full_charge_capacities = [int(entry['FullChargeCapacity']) for entry in recent_usage]
    design_capacity = int(battery_info[0]['DesignCapacity']) if battery_info else 0
    
    # Plot battery capacity over time
    fig1.clear()
    ax1 = fig1.add_subplot(111)
    ax1.plot(timestamps, charge_capacities, label='Charge Capacity')
    ax1.plot(timestamps, full_charge_capacities, label='Full Charge Capacity')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Capacity (mWh)')
    ax1.set_title('Battery Capacity Over Time')
    ax1.legend()
    ax1.xaxis.set_major_locator(plt.MaxNLocator(6))
    fig1.autofmt_xdate()
    fig1.tight_layout()
    canvas1.draw()
    
    # Plot overall battery health
    health_values = [calculate_battery_health(battery) for battery in battery_info]
    labels = [battery['Id'] for battery in battery_info]
    
    fig2.clear()
    ax2 = fig2.add_subplot(111)
    ax2.bar(labels, health_values, color='green')
    ax2.set_xlabel('Battery')
    ax2.set_ylabel('Health (%)')
    ax2.set_title('Battery Health')
    fig2.tight_layout()
    canvas2.draw()

    # Plot historical battery health
    historical_health = calculate_historical_health(recent_usage, design_capacity)
    
    fig3.clear()
    ax3 = fig3.add_subplot(111)
    ax3.plot(timestamps, historical_health, label='Historical Health', color='blue')
    ax3.set_xlabel('Timestamp')
    ax3.set_ylabel('Health (%)')
    ax3.set_title('Historical Battery Health')
    ax3.legend()
    ax3.xaxis.set_major_locator(plt.MaxNLocator(6))
    fig3.autofmt_xdate()
    fig3.tight_layout()
    canvas3.draw()
    
    # Plot cycle count over time
    cycle_counts = calculate_cycle_count_over_time(recent_usage)
    
    fig4.clear()
    ax4 = fig4.add_subplot(111)
    if cycle_counts:
        ax4.plot(timestamps, cycle_counts, label='Cycle Count', color='purple')
    ax4.set_xlabel('Timestamp')
    ax4.set_ylabel('Cycle Count')
    ax4.set_title('Battery Cycle Count Over Time')
    ax4.legend()
    ax4.xaxis.set_major_locator(plt.MaxNLocator(6))
    fig4.autofmt_xdate()
    fig4.tight_layout()
    canvas4.draw()
    
    # Plot discharge rate over time
    discharge_rates = calculate_discharge_rate(recent_usage)
    
    fig5.clear()
    ax5 = fig5.add_subplot(111)
    if discharge_rates:
        ax5.plot(timestamps[:len(discharge_rates)], discharge_rates, label='Discharge Rate', color='red')
    ax5.set_xlabel('Timestamp')
    ax5.set_ylabel('Discharge Rate')
    ax5.set_title('Battery Discharge Rate Over Time')
    ax5.legend()
    ax5.xaxis.set_major_locator(plt.MaxNLocator(6))
    fig5.autofmt_xdate()
    fig5.tight_layout()
    canvas5.draw()

    # Plot energy consumption over time
    energy_consumption = calculate_energy_consumption(recent_usage)
    
    fig6.clear()
    ax6 = fig6.add_subplot(111)
    if isinstance(energy_consumption, list):
        ax6.plot(timestamps[:len(energy_consumption)], energy_consumption, label='Energy Consumption', color='orange')
    ax6.set_xlabel('Timestamp')
    ax6.set_ylabel('Energy (mWh)')
    ax6.set_title('Energy Consumption Over Time')
    ax6.legend()
    ax6.xaxis.set_major_locator(plt.MaxNLocator(6))
    fig6.autofmt_xdate()
    fig6.tight_layout()
    canvas6.draw()

    # Plot average discharge rate
    average_discharge_rate = calculate_average_discharge_rate(recent_usage)
    
    fig7.clear()
    ax7 = fig7.add_subplot(111)
    ax7.bar(['Average Discharge Rate'], [average_discharge_rate], color='blue')
    ax7.set_ylabel('Discharge Rate')
    ax7.set_title('Average Discharge Rate')
    fig7.tight_layout()
    canvas7.draw()

    # Plot charge/discharge cycles
    charge_discharge_cycles = count_charge_discharge_cycles(recent_usage)
    
    fig8.clear()
    ax8 = fig8.add_subplot(111)
    ax8.bar(['Charge/Discharge Cycles'], [charge_discharge_cycles], color='green')
    ax8.set_ylabel('Cycles')
    ax8.set_title('Charge/Discharge Cycles')
    fig8.tight_layout()
    canvas8.draw()

    # Plot estimated time to full charge and to empty
    current_capacity = charge_capacities[-1] if charge_capacities else 0
    full_charge_capacity = full_charge_capacities[-1] if full_charge_capacities else 0
    average_discharge_rate = calculate_average_discharge_rate(recent_usage)  # Make sure the discharge rate is negative of charge rate
    
    time_to_full_charge = estimate_time_to_full_charge(current_capacity, full_charge_capacity, average_discharge_rate)
    time_to_empty = estimate_time_to_empty(current_capacity, average_discharge_rate)
    
    fig9.clear()
    ax9 = fig9.add_subplot(111)
    ax9.bar(['Time to Full Charge', 'Time to Empty'], [time_to_full_charge, time_to_empty], color=['blue', 'red'])
    ax9.set_ylabel('Time (hours)')
    ax9.set_title('Estimated Time to Full Charge and Empty')
    fig9.tight_layout()
    canvas9.draw()
