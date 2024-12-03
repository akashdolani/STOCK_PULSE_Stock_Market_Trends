# Analyze Stock Market Trends

## Group Members
- Akash Dolani    KU2407U009
- Angel Yadav     KU2407U014
- Ayush Trivedi   KU2407U029
- Adwait Sonekar  KU2407U008

## Objective of the Project
The objective of this project is to analyze stock market trends by visualizing historical stock prices and computing key indicators such as 5-day and 10-day moving averages. 
This tool provides insights into stock performance and enables comparisons between different stocks. The project aims to develop a tool that helps users understand and analyze the performance 
of stocks over time. This is achieved by visualizing historical stock prices, calculating essential metrics like 5-day and 10-day moving averages, and enabling trend comparisons across multiple 
stocks. The project aims to provide users, including students, investors, and researchers, with a user-friendly interface to explore stock data, identify trends, and make data-driven 
observations. By integrating interactive visualizations and multiple analysis modes, the tool allows for a deeper understanding of market dynamics and stock behavior.

## Tools and Libraries Used
- Programming Language: Python
- Libraries:
  - PANDAS: For data manipulation and analysis.
  - MATPLOTLIB: For creating static, animated, and interactive visualizations.
  - TKINTER: For building the graphical user interface (GUI).

## Data Source(s)
- The stock dataset was sourced from [Kaggle](https://www.kaggle.com/) and stored in a CSV file named `data1.csv`. 
- The dataset contains the following columns:
  - Date (MM-DD-YYYY format)
  - Stock (Stock name)
  - Close (Closing price of the stock in USD)
## Execution Steps
1. Prepare the Environment:
   - Ensure Python 3.9 is installed.
   - Install required libraries using:
     ```bash
     pip install pandas matplotlib
     ```
2. Place the Data File:
   - Save your `data_1.csv` file in the specified directory:  
     `C:\\Users\\Akash\\OneDrive\\documents\\college\\sem-1\\PROJECTS\\AI\\data\\`

3. Run the Application:
   - Execute the Python script:
   - ```bash
     python <stock_market_trends>.py
     ```
4. Interact with the GUI:
   - Choose an analysis type (Single Stock Trend, Comparison, Moving Averages, All Stocks).
   - Select stock(s) from the dropdown menus.
   - Click Analyze to generate the desired plots.

## Summary of Results
The application provides:
- Trend analysis for individual stocks.
- Comparison between two selected stocks.
- Moving average analysis (5-day and 10-day) for one or two stocks.
- Visualization of trends for all stocks in the dataset.

## Challenges Faced
- Finding a Proper Dataset:Identifying a dataset that met the requirements of the project was challenging, as it needed to contain consistent and clean data with historical stock prices
  for multiple stocks. Kaggle was eventually chosen as the source for its reliability and variety of datasets.
- Data Preprocessing: Handling the formatting of dates and numeric conversion for financial data.
- GUI Design: Creating an intuitive interface for users with minimal experience.
- Error Handling: Ensuring the application handles invalid inputs gracefully without crashing.
- Dynamic Visualizations: Embedding Matplotlib plots into a Tkinter GUI while maintaining responsiveness.
