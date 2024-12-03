import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

class StockAnalysisApp:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        master.title("Stock Analysis Tool")
        master.geometry("800x600")

        # Load and preprocess data
        self.load_data()

        # Create GUI elements
        self.create_widgets()

    def load_data(self):
        # Load dataset
        file_path = "C:\\Users\\Akash\\OneDrive\\ドキュメント\\college\\sem-1\\PROJECTS\\AI\\data\\data_1.csv"
        self.df = pd.read_csv(file_path)
        
        # Preprocess data
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%m-%d-%Y')
        self.df = self.df.sort_values(by=['Stock', 'Date'])
        self.df['Close'] = self.df['Close'].replace('[\$,]', '', regex=True).astype(float)
        
        # Calculate moving averages for each stock
        self.df['5-Day MA'] = self.df.groupby('Stock')['Close'].transform(lambda x: x.rolling(window=5).mean())
        self.df['10-Day MA'] = self.df.groupby('Stock')['Close'].transform(lambda x: x.rolling(window=10).mean())

        # Get unique stock names
        self.stocks = self.df['Stock'].unique().tolist()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Analysis Type Radiobuttons
        self.analysis_type = tk.StringVar(value="single_trend")
        ttk.Label(main_frame, text="Select Analysis Type:").grid(row=0, column=0, sticky=tk.W)
        analysis_types = [
            ("Single Stock Trend", "single_trend"),
            ("Stock Comparison", "comparison"),
            ("Moving Averages", "moving_avg"),
            ("All Stocks Trend", "all_stocks")
        ]
        
        # Create radio buttons
        for i, (text, value) in enumerate(analysis_types):
            ttk.Radiobutton(
                main_frame, 
                text=text, 
                variable=self.analysis_type, 
                value=value, 
                command=self.update_stock_selection
            ).grid(row=0, column=i+1, sticky=tk.W)

        # Stock Selection Dropdowns
        ttk.Label(main_frame, text="Select Stock(s):").grid(row=1, column=0, sticky=tk.W)
        
        # Single Stock Dropdown
        self.single_stock_var = tk.StringVar()
        self.single_stock_dropdown = ttk.Combobox(main_frame, textvariable=self.single_stock_var, values=self.stocks, state="readonly", width=15)
        self.single_stock_dropdown.grid(row=2, column=0, padx=5, pady=5)
        self.single_stock_dropdown.set("Select Stock")

        # Comparison Stock Dropdowns
        self.stock1_var = tk.StringVar()
        self.stock2_var = tk.StringVar()
        self.stock1_dropdown = ttk.Combobox(main_frame, textvariable=self.stock1_var, values=self.stocks, state="disabled", width=15)
        self.stock2_dropdown = ttk.Combobox(main_frame, textvariable=self.stock2_var, values=self.stocks, state="disabled", width=15)
        self.stock1_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.stock2_dropdown.grid(row=2, column=2, padx=5, pady=5)
        self.stock1_dropdown.set("Select First Stock")
        self.stock2_dropdown.set("Select Second Stock")

        # Analyze Button
        ttk.Button(main_frame, text="Analyze", command=self.analyze_stocks).grid(row=3, column=0, columnspan=4, pady=10)

        # Plot Frame
        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initial update to set correct state
        self.update_stock_selection()

    def update_stock_selection(self):
        analysis_type = self.analysis_type.get()

        # Reset all dropdowns
        self.single_stock_dropdown.set("Select Stock")
        self.stock1_dropdown.set("Select First Stock")
        self.stock2_dropdown.set("Select Second Stock")

        if analysis_type == "single_trend":
            self.single_stock_dropdown.config(state="readonly")
            self.stock1_dropdown.config(state="disabled")
            self.stock2_dropdown.config(state="disabled")

        elif analysis_type == "comparison":
            self.single_stock_dropdown.config(state="disabled")
            self.stock1_dropdown.config(state="readonly")
            self.stock2_dropdown.config(state="readonly")

        elif analysis_type == "moving_avg":
            self.single_stock_dropdown.config(state="disabled")
            self.stock1_dropdown.config(state="readonly")
            self.stock2_dropdown.config(state="readonly")

        elif analysis_type == "all_stocks":
            self.single_stock_dropdown.config(state="disabled")
            self.stock1_dropdown.config(state="disabled")
            self.stock2_dropdown.config(state="disabled")
    def analyze_stocks(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        analysis_type = self.analysis_type.get()

        try:
            if analysis_type == "single_trend":
                stock = self.single_stock_var.get()
                if stock == "Select Stock":
                    messagebox.showerror("Error", "Please select a stock")
                    return
                self.plot_stock_trend(stock)

            elif analysis_type == "comparison":
                stock1 = self.stock1_var.get()
                stock2 = self.stock2_var.get()
                if stock1 == "Select First Stock" or stock2 == "Select Second Stock":
                    messagebox.showerror("Error", "Please select two stocks")
                    return
                self.compare_stocks(stock1, stock2)

            elif analysis_type == "moving_avg":
                stock1 = self.stock1_var.get()
                stock2 = self.stock2_var.get()
                if stock1 == "Select First Stock" and stock2 == "Select Second Stock":
                    messagebox.showerror("Error", "Please select at least one stock")
                    return

                if stock1 == "Select First Stock" or stock2 == "Select Second Stock":
                    stock = stock1 if stock1 != "Select First Stock" else stock2
                    self.plot_moving_averages(stock)
                else:
                    self.compare_moving_averages(stock1, stock2)

            elif analysis_type == "all_stocks":
                self.plot_all_stocks_trend()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_stock_trend(self, stock):
        stock_data = self.df[self.df['Stock'] == stock]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data['Date'], stock_data['Close'], label='Closing Price', marker='o', color='blue')
        #ax.plot(stock_data['Date'], stock_data['5-Day MA'], label='5-Day Moving Average', linestyle='--', color='orange')
        #ax.plot(stock_data['Date'], stock_data['10-Day MA'], label='10-Day Moving Average', linestyle='--', color='green')
        ax.set_title(f'Stock Price Trend for {stock}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        self.embed_plot(fig)

    def compare_stocks(self, stock1, stock2):
        stock1_data = self.df[self.df['Stock'] == stock1]
        stock2_data = self.df[self.df['Stock'] == stock2]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock1_data['Date'], stock1_data['Close'], label=f'{stock1} Closing Price', marker='o', color='blue')
        ax.plot(stock2_data['Date'], stock2_data['Close'], label=f'{stock2} Closing Price', marker='o', color='red')
        ax.set_title(f'Comparison of {stock1} and {stock2}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        self.embed_plot(fig)
    def compare_moving_averages(self, stock1, stock2):
        stock1_data = self.df[self.df['Stock'] == stock1]
        stock2_data = self.df[self.df['Stock'] == stock2]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock1_data['Date'], stock1_data['5-Day MA'], label=f'{stock1} 5-Day MA', linestyle='--', color='orange')
        ax.plot(stock1_data['Date'], stock1_data['10-Day MA'], label=f'{stock1} 10-Day MA', linestyle='-', color='green')
        ax.plot(stock2_data['Date'], stock2_data['5-Day MA'], label=f'{stock2} 5-Day MA', linestyle='--', color='blue')
        ax.plot(stock2_data['Date'], stock2_data['10-Day MA'], label=f'{stock2} 10-Day MA', linestyle='-', color='red')
        
        ax.set_title(f'Moving Averages Comparison: {stock1} vs {stock2}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        self.embed_plot(fig)


    def plot_moving_averages(self, stock):
        stock_data = self.df[self.df['Stock'] == stock]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data['Date'], stock_data['5-Day MA'], label='5-Day Moving Average', linestyle='--', color='orange')
        ax.plot(stock_data['Date'], stock_data['10-Day MA'], label='10-Day Moving Average', linestyle='--', color='green')
        ax.set_title(f'Moving Averages for {stock}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        self.embed_plot(fig)

    def plot_all_stocks_trend(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        for stock in self.stocks:
            stock_data = self.df[self.df['Stock'] == stock]
            ax.plot(stock_data['Date'], stock_data['Close'], label=stock, marker='o')
            ax.plot(stock_data['Date'], stock_data['5-Day MA'], label=f'{stock} 5-Day MA', linestyle='--')
            ax.plot(stock_data['Date'], stock_data['10-Day MA'], label=f'{stock} 10-Day MA', linestyle='--')
        ax.set_title('Trends of All Stocks')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend(title='Stocks', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.embed_plot(fig)

    def embed_plot(self, fig):
        # Embed matplotlib plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas.draw()

   
def main():
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
