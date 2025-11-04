# modules/data_visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import os

class DataVisualizer:
    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def plot_bar(self, df, x_col, y_col, title="Bar Chart"):
        """Creates and saves a bar chart"""
        try:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=x_col, y=y_col, data=df)
            plt.title(title)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            output_path = os.path.join(self.output_folder, f"BarChart_{y_col}_by_{x_col}.png")
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Bar chart saved at: {output_path}")
        except Exception as e:
            print(f"❌ Error while plotting bar chart: {e}")

    def plot_line(self, df, x_col, y_col, title="Line Chart"):
        """Creates and saves a line chart"""
        try:
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=x_col, y=y_col, data=df, marker='o')
            plt.title(title)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            output_path = os.path.join(self.output_folder, f"LineChart_{y_col}_over_{x_col}.png")
            plt.savefig(output_path)
            plt.close()
            print(f"✅ Line chart saved at: {output_path}")
        except Exception as e:
            print(f"❌ Error while plotting line chart: {e}")
