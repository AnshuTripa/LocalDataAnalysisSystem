# main.py
import pandas as pd
from modules.data_loader import DataLoader
from modules.data_analyzer import DataAnalyzer
from modules.data_visualizer import DataVisualizer
from modules.nlp_query import QueryEngine
from modules.report_generator import ReportGenerator

if __name__ == "__main__":
    print("🔧 LOCAL DATA ANALYSIS SYSTEM\n")

    # --- STEP 1: LOAD & CLEAN DATA FILES ---
    loader = DataLoader(data_folder="data")
    loader.load_and_clean_files()

    # --- STEP 2: ANALYZE DATA ---
    analyzer = DataAnalyzer(cleaned_data_folder="output")
    analyzer.analyze_all()

    print("\n✅ All files analyzed successfully! Check the 'output/' folder for reports and graphs.")

    # --- STEP 3: LOAD ONE FILE ---
    file_path = "data/Ship1 maintenance history Sep23-Aug25.xlsx"
    df = pd.read_excel(file_path)

    # Clean column names
    df.columns = df.columns.str.replace(r'[\n\r\t]+', '', regex=True).str.strip()
    print("\n✅ Cleaned Columns:", list(df.columns))

    # --- STEP 4: VISUALIZE DATA ---
    viz = DataVisualizer()

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    non_numeric_cols = df.select_dtypes(exclude='number').columns.tolist()

    print("\n📊 Numeric columns detected:", numeric_cols[:5])
    print("🗂️ Non-numeric columns detected:", non_numeric_cols[:5])

    if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
        x_col = non_numeric_cols[0]
        y_col = numeric_cols[0]
        viz.plot_bar(df, x_col=x_col, y_col=y_col, title=f"Bar Chart: {y_col} by {x_col}")
        viz.plot_line(df, x_col=x_col, y_col=y_col, title=f"Line Chart: {y_col} over {x_col}")
    else:
        print("❌ Not enough valid columns for visualization.")

    # --- STEP 5: NLP QUERY (OPTIONAL INTERACTIVE PART) ---
    qe = QueryEngine(df)
    print("\n💬 Type your query (type 'exit' to quit):")
    while True:
        query = input(">> ")
        if query.lower() in ["exit", "quit"]:
            break
        response = qe.process_query(query)
        print(response)

    # --- STEP 6: REPORT GENERATION ---
    print("\n📘 Generating final PDF report...")
    report = ReportGenerator(df)
    report.generate_pdf()
    print("\n✅ Report generated successfully! Check the 'output/' folder.")
 