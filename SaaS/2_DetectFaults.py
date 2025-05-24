import pandas as pd
import os

def detect_and_export_faults(input_file_path, output_folder):
    df = pd.read_csv(input_file_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    faults = {}
    
    # Missing Meter ID
    missing_meter_id = df[df['MeterID'].isna() | (df['MeterID'] == "")]
    faults['Missing Meter ID'] = len(missing_meter_id)
    if not missing_meter_id.empty:
        missing_meter_id.to_csv(f"{output_folder}/missing_meter_id.csv", index=False)
    
    # Invalid Meter ID (special chars or lowercase letters)
    invalid_meter_id = df[df['MeterID'].str.contains(r'[^A-Z0-9]', regex=True, na=False)]
    faults['Invalid Meter ID (special chars or lowercase)'] = len(invalid_meter_id)
    if not invalid_meter_id.empty:
        invalid_meter_id.to_csv(f"{output_folder}/invalid_meter_id.csv", index=False)
    
    # Future Service Start Date
    service_dates = pd.to_datetime(df['ServiceStartDate'], errors='coerce')
    future_start_date = df[service_dates > pd.Timestamp.today()]
    faults['Future Service Start Date'] = len(future_start_date)
    if not future_start_date.empty:
        future_start_date.to_csv(f"{output_folder}/future_start_date.csv", index=False)
    
    # Invalid Email format
    invalid_email = df[~df['Email'].str.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', na=False)]
    faults['Invalid Email'] = len(invalid_email)
    if not invalid_email.empty:
        invalid_email.to_csv(f"{output_folder}/invalid_email.csv", index=False)
    
    # Invalid Phone format (should be exactly 10 digits)
    invalid_phone = df[~df['Phone'].str.match(r'^\d{10}$', na=False)]
    faults['Invalid Phone'] = len(invalid_phone)
    if not invalid_phone.empty:
        invalid_phone.to_csv(f"{output_folder}/invalid_phone.csv", index=False)
    
    # Write summary to text file
    summary_file = os.path.join(output_folder, "fault_summary.txt")
    with open(summary_file, 'w') as f:
        total_faulty = sum(faults.values())
        f.write(f"Total faulty records: {total_faulty}\n\n")
        for fault, count in faults.items():
            f.write(f"{fault}: {count} record(s)\n")
    
    # Print summary in console
    print("Faults Detected and exported:")
    for fault, count in faults.items():
        print(f"{fault}: {count} record(s)")
    
    return faults

# Usage example:
input_file = r"C:\Users\Dell\Documents\SaaS\Database\customer_data_smart360.csv"
output_dir = r"C:\Users\Dell\Documents\SaaS\FaultyRecords"

detect_and_export_faults(input_file, output_dir)
