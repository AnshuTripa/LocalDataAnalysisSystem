# modules/data_loader.py
import pandas as pd
import os

class DataLoader:
    def __init__(self, data_folder, output_folder="output"):
        self.data_folder = data_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def clean_dataframe(self, df):
        """
        Cleans a DataFrame by removing empty and unnamed columns.
        """
        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Drop fully empty rows and columns
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all')
        # Remove extra spaces and line breaks in column names
        df.columns = df.columns.str.replace('\n', ' ').str.strip()
        df.columns = df.columns.str.replace(' +', ' ', regex=True)
        return df

    def load_and_clean_files(self):
        """
        Loads, cleans, and saves each Excel/CSV file individually.
        """
        files = [f for f in os.listdir(self.data_folder) if f.endswith(('.xlsx', '.csv'))]
        print(f"\n📂 Found {len(files)} files: {files}\n")

        for file in files:
            file_path = os.path.join(self.data_folder, file)
            print(f"➡️ Loading and cleaning: {file}")
            
            # Load file
            if file.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            # Clean file
            df_clean = self.clean_dataframe(df)

            # Save cleaned version
            output_path = os.path.join(self.output_folder, f"cleaned_{file}")
            df_clean.to_excel(output_path, index=False)
            print(f"   ✅ Cleaned file saved as {output_path} ({len(df_clean)} rows, {len(df_clean.columns)} columns)\n")

        print("🎯 All files cleaned and saved successfully!")
