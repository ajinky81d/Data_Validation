import pandas as pd
import os

# Paths
original_path = r"C:\Users\Dell\Documents\SaaS\1_Uploaded_File\customer_data_smart360.csv"
corrected_folder = r"C:\Users\Dell\Documents\SaaS\3_Corrected_Files"
output_folder = r"C:\Users\Dell\Documents\SaaS\4_Cleaned_File"
output_file = os.path.join(output_folder, "updated_customer_data_smart360.csv")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load original dataset
df_original = pd.read_csv(original_path)

# Load corrected records
corrected_missing = pd.read_csv(os.path.join(corrected_folder, "corrected_missing_meter_id.csv"))
corrected_meter = pd.read_csv(os.path.join(corrected_folder, "corrected_invalid_meter_id.csv"))
corrected_date = pd.read_csv(os.path.join(corrected_folder, "corrected_future_start_date.csv"))
corrected_email = pd.read_csv(os.path.join(corrected_folder, "corrected_invalid_email.csv"))
corrected_phone = pd.read_csv(os.path.join(corrected_folder, "corrected_invalid_phone.csv"))

# Combine corrected data
corrected_all = pd.concat([
    corrected_missing,
    corrected_meter,
    corrected_date,
    corrected_email,
    corrected_phone
], ignore_index=True)

# Replace faulty entries in original dataset
if 'CustomerID' in df_original.columns:
    df_cleaned = df_original[~df_original['CustomerID'].isin(corrected_all['CustomerID'])]
    df_cleaned = pd.concat([df_cleaned, corrected_all], ignore_index=True)
else:
    raise Exception("CustomerID column not found for matching records.")

# Save to output folder
df_cleaned.to_csv(output_file, index=False)
print(f"✅ Cleaned file saved at: {output_file}")
