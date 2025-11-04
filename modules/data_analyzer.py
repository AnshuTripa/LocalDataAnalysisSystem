# modules/data_analyzer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class DataAnalyzer:
    def __init__(self, cleaned_data_folder, output_folder="output"):
        self.cleaned_data_folder = cleaned_data_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    def load_cleaned_files(self):
        """
        Loads all cleaned Excel files for analysis.
        """
        files = [f for f in os.listdir(self.cleaned_data_folder) if f.startswith("cleaned_") and f.endswith(".xlsx")]
        dataframes = {}

        print(f"\n📊 Found {len(files)} cleaned files: {files}\n")

        for file in files:
            path = os.path.join(self.cleaned_data_folder, file)
            df = pd.read_excel(path)
            dataframes[file] = df
            print(f"✅ Loaded {file}: {df.shape[0]} rows, {df.shape[1]} columns")

        return dataframes

    def describe_data(self, df, file_name):
        """
        Saves basic statistics summary for a DataFrame.
        """
        summary = df.describe(include='all')
        summary_path = os.path.join(self.output_folder, f"summary_{file_name}.xlsx")
        summary.to_excel(summary_path)
        print(f"📈 Summary saved: {summary_path}")

    def numeric_analysis(self, df, file_name):
        """
        Finds correlation between numeric columns.
        """
        numeric_df = df.select_dtypes(include='number')

        if numeric_df.empty:
            print(f"⚠️ No numeric columns found in {file_name}")
            return

        corr = numeric_df.corr()
        corr_path = os.path.join(self.output_folder, f"correlation_{file_name}.xlsx")
        corr.to_excel(corr_path)
        print(f"📊 Correlation matrix saved: {corr_path}")

        # Plot correlation heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title(f'Correlation Heatmap - {file_name}')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_folder, f"heatmap_{file_name}.png"))
        plt.close()
        print(f"🖼️ Heatmap saved as heatmap_{file_name}.png")

    def visualize_columns(self, df, file_name):
        """
        Generates simple visualizations for numeric data.
        """
        numeric_cols = df.select_dtypes(include='number').columns
        if numeric_cols.empty:
            print(f"⚠️ No numeric data for charts in {file_name}")
            return

        for col in numeric_cols[:5]:  # limit to first 5 columns for simplicity
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f'{col} Distribution')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.tight_layout()

            save_path = os.path.join(self.output_folder, f"{file_name}_{col}_hist.png")
            plt.savefig(save_path)
            plt.close()
            print(f"📊 Histogram saved: {save_path}")

    def analyze_all(self):
        """
        Performs full analysis for all cleaned files.
        """
        dataframes = self.load_cleaned_files()

        for file_name, df in dataframes.items():
            print(f"\n🔍 Analyzing {file_name}...")
            self.describe_data(df, file_name)
            self.numeric_analysis(df, file_name)
            self.visualize_columns(df, file_name)
            print(f"✅ Analysis completed for {file_name}\n")
