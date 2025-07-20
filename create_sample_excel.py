import pandas as pd
import numpy as np

# Create sample data
data = {
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'UDISE': ['12345', '67890', '11111', '22222', '33333']
}

# Add OPTION columns with random preferences
for i in range(1, 31):
    # Generate random preferences (1-30) for each person
    preferences = np.random.permutation(30) + 1
    data[f'OPTION{i}'] = preferences

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
df.to_excel('sample_data.xlsx', index=False)

print("Sample Excel file 'sample_data.xlsx' created successfully!")
print(f"File contains {len(df)} people with preferences for 30 options.")
print("The last row represents the current user.")
print("\nColumns in the file:")
print(df.columns.tolist()) 