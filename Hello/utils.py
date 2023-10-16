import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import logging 

logger = logging.getLogger(__name__)

def process_and_visualize_excel(file, chart_type):
    try:
        # Step 1: Read the Excel file
        df = pd.read_excel(file)
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return None

    # Step 2: Automatically identify the "Category" and "Values" columns
    category_column = None
    values_column = None

    for column in df.columns:
        if df[column].dtype == 'object':
            category_column = column
        elif df[column].dtype in ['int64', 'float64']:
            values_column = column

    if category_column and values_column:
        # Step 3: Use the identified "Category" and "Values" columns
        category_data = df[category_column]
        values_data = df[values_column]

        # Generate the specified chart type
        plt.figure(figsize=(8, 6))
        if chart_type == 'Bar Chart':
            plt.bar(category_data, values_data)
        elif chart_type == 'Line Graph':
            plt.plot(category_data, values_data, marker='o')
        elif chart_type == 'Pie Chart':
            plt.pie(values_data, labels=category_data, autopct='%1.1f%%', startangle=140)
        elif chart_type == 'Histogram':
            plt.hist(values_data, bins=10)
        plt.xlabel(category_column)
        plt.ylabel(values_column)
        plt.title(chart_type)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return image_base64  # Return the chart image as a base64 string
    else:
        # Log that category and values columns could not be identified
        logger.error("Unable to identify 'Category' and 'Values' columns")
        return None