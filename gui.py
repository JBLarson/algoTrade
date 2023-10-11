import sys
import json
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QScrollArea, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from tickers import tickers  # Assuming tickers.py is in the same directory and contains your tickers list

class App(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Stock Data Viewer")
		self.setGeometry(100, 100, 1200, 800)
		
		main_layout = QHBoxLayout()
		
		button_widget = QWidget()
		button_layout = QVBoxLayout(button_widget)
		
		# This loop should be inside __init__ method
		for ticker in tickers:
			button = QPushButton(ticker)
			button.clicked.connect(self.create_plotter(ticker))  # Using a method that returns a method to avoid the capturing issue
			button_layout.addWidget(button)

		scroll = QScrollArea()
		scroll.setWidget(button_widget)
		scroll.setWidgetResizable(True)
		scroll.setFixedWidth(200)
		
		self.figure = Figure(figsize=(10, 8))
		self.canvas = FigureCanvas(self.figure)
		
		main_layout.addWidget(scroll)
		main_layout.addWidget(self.canvas)
		
		main_widget = QWidget()
		main_widget.setLayout(main_layout)
		self.setCentralWidget(main_widget)

	def create_plotter(self, ticker):
		return lambda: self.plot_stock_data(ticker)

	def plot_stock_data(self, ticker):
		filepath = f"stockData/{ticker}.json"
		
		try:
			# Load the data from the JSON file
			with open(filepath, 'r') as file:
				data = json.load(file)
			
			# Extract the dates, prices, and volumes from the data
			dates = [item["Date"] for item in data]
			prices = [item["Close"] for item in data]
			volumes = [item["Volume"] for item in data]
			
			# Clear the existing figure
			self.figure.clear()
			
			ax1 = self.figure.add_subplot(211)
			ax1.plot(dates, prices, marker='o', label="Price")
			ax1.set_title(f"{ticker} - Price and Volume Over Time")
			ax1.set_ylabel("Price")
			ax1.legend()
			
			ax2 = self.figure.add_subplot(212)
			ax2.bar(dates, volumes, label="Volume")
			ax2.set_xlabel("Date")
			ax2.set_ylabel("Volume")
			ax2.legend()
			
			# Draw the new plot
			self.canvas.draw()
		
		except FileNotFoundError:
			print(f"No data file found for {ticker}.")
		except json.JSONDecodeError:
			print(f"Error decoding the JSON file for {ticker}.")
		except KeyError as e:
			print(f"Expected key {str(e)} not found in the JSON file for {ticker}.")
		except Exception as e:
			print(f"An unexpected error occurred: {str(e)}")
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = App()
	window.show()
	sys.exit(app.exec_())
