import pandas as pd

def correct_totals(csv_path, output_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # List of columns that contain daily box office totals
    daily_columns = [f'Day{i}BoxOffice' for i in range(1, 31)]
    
    # Initialize a column for concurrent totals
    df['Day1ToDate'] = df['Day1BoxOffice']

    # Calculate concurrent totals for each day
    for i in range(1, 30):
        df[f'Day{i+1}ToDate'] = df[daily_columns[:i+1]].sum(axis=1)

    # Write the corrected data to a new CSV file
    df.to_csv(output_path, index=False)

# Usage
csv_path = 'bad_data.csv'  # Replace with your CSV file path
output_path = 'corrected_data.csv'
correct_totals(csv_path, output_path)