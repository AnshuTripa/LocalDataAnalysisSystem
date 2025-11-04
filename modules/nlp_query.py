import re
import pandas as pd
from modules.data_visualizer import DataVisualizer

class QueryEngine:
    def __init__(self, df):
        self.df = df
        self.viz = DataVisualizer()

    def process_query(self, query: str):
        query = query.lower().strip()

        # 🔹 1. Show all columns
        if "columns" in query or "show columns" in query:
            return f"Columns in dataset:\n{list(self.df.columns)}"

        # 🔹 2. Count total rows
        elif "total" in query and ("rows" in query or "records" in query):
            return f"Total records: {len(self.df)}"

        # 🔹 3. Average of a column
        match = re.search(r"average (\w+)", query)
        if match:
            col = self.find_column(match.group(1))
            if col:
                return f"Average of '{col}' = {self.df[col].mean():.2f}"
            else:
                return "❌ Column not found."

        # 🔹 4. Count by a category
        match = re.search(r"show (.+) by (.+)", query)
        if match:
            y_col = self.find_column(match.group(1))
            x_col = self.find_column(match.group(2))
            if y_col and x_col:
                grouped = self.df.groupby(x_col)[y_col].count().reset_index()
                self.viz.plot_bar(grouped, x_col=x_col, y_col=y_col, title=f"{y_col} by {x_col}")
                return f"✅ Chart generated: {y_col} by {x_col}"
            else:
                return "❌ Could not interpret columns."

        # 🔹 5. Show unique values
        match = re.search(r"unique (.+)", query)
        if match:
            col = self.find_column(match.group(1))
            if col:
                return f"Unique values in '{col}':\n{self.df[col].unique()}"
            else:
                return "❌ Column not found."

        else:
            return "🤔 Sorry, I didn’t understand that query. Try:\n - 'show total maintenance by user'\n - 'average done unit'\n - 'unique service'"

    def find_column(self, keyword):
        for col in self.df.columns:
            if keyword.lower() in col.lower():
                return col
        return None
