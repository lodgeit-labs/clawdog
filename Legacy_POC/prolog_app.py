import tkinter as tk
import subprocess

def run_neurosymbolic_engine():
    # Clear the text box for a fresh run
    output_text.delete(1.0, tk.END) 
    output_text.insert(tk.END, "Initiating L402 Paywall Check...\n")
    output_text.update()
    
    # 1. SIMULATE L402 LIGHTNING PAYMENT
    l402_paid = True 
    if not l402_paid:
        output_text.insert(tk.END, "ERROR: 402 Payment Required. Please pay 50 sats.\n")
        return
        
    output_text.insert(tk.END, "L402 Validated (50 sats). Executing Prolog Engine...\n")
    output_text.update()

    # 2. THE ZERO-RISK PROLOG SUBPROCESS
    # This calls the SWI-Prolog executable in the background
    prolog_command = [
        "swipl", 
        "-q", # Quiet mode
        "-s", "C:/Users/futur/Documents/LodgeiT_Global/02_Rules/gst_tax_rules.pl",
        "-s", "C:/Users/futur/Documents/LodgeiT_Global/02_Rules/sbrm_kb.pl",
        "-g", "calculate_iawo_deduction('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026', Deduction), writeln(Deduction).",
        "-t", "halt" # Closes Prolog instantly to prevent memory leaks
    ]

    try:
        # 3. FIRE THE ENGINE AND CAPTURE RESULT
        result = subprocess.run(prolog_command, capture_output=True, text=True, check=True)
        iawo_deduction = result.stdout.strip()
        
        output_text.insert(tk.END, f"\nSUCCESS: Engine cross-referenced SBRM & GST rules.\n")
        output_text.insert(tk.END, f"Approved IAWO Deduction: ${iawo_deduction}\n")
        
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"\nPROLOG ERROR:\n{e.stderr}\n")
    except FileNotFoundError:
        output_text.insert(tk.END, "\nSYSTEM ERROR: Could not find 'swipl'. Please make sure SWI-Prolog is installed.\n")

# --- GUI WINDOW SETUP ---
root = tk.Tk()
root.title("ClientRelay - L402 & SBRM Engine")
root.geometry("550x350")

title_label = tk.Label(root, text="Neurosymbolic Tax Deduction Engine", font=("Helvetica", 14, "bold"))
title_label.pack(pady=15)

# The Execution Button
run_button = tk.Button(root, text="Pay 50 Sats & Calculate IAWO", command=run_neurosymbolic_engine, font=("Helvetica", 12), bg="#d4edda")
run_button.pack(pady=10)

# The Output Console
output_text = tk.Text(root, height=10, width=60, font=("Courier", 10), bg="#f8f9fa")
output_text.pack(pady=15)

# Start the application loop
root.mainloop()