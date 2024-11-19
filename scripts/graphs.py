import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv("station_data_statistics.csv")

# Extract year and station from "Station_Year" column
data[['Station', 'Year']] = data['Station_Year'].str.split('_', expand=True)
data['Year'] = data['Year'].astype(int)  # Convert year to integer for sorting

# Define the metrics to plot
metrics = ['WVHT', 'DPD', 'WTMP']
stats = ['mean', 'median']

# Create graphs for each metric and statistic
for stat in stats:
    for metric in metrics:
        column_name = f"{metric}_{stat}"
        
        # Compute the average of the metric for each station
        station_averages = data.groupby("Station")[column_name].mean().sort_values(ascending=False)
        
        # Select the top 10 stations
        top_stations = station_averages.head(10).index
        
        # Filter the data for the top 10 stations
        filtered_data = data[data['Station'].isin(top_stations)]
        
        # Prepare the plot
        plt.figure(figsize=(12, 6))
        plt.title(f"{metric} ({stat.capitalize()}) Over Time (Top 10 Stations)")
        plt.xlabel("Year")
        plt.ylabel(f"{metric} ({stat.capitalize()})")
        
        # Plot lines for the top 10 stations
        for station, group in filtered_data.groupby("Station"):
            # Extract the data for this station and sort by year
            station_data = group.sort_values("Year")
            plt.plot(station_data["Year"], station_data[column_name], label=f"Station {station}")
        
        # Add legend and grid
        plt.legend(title="Station", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(visible=True, linestyle='--', alpha=0.5)
        
        # Save each graph
        plt.tight_layout()
        plt.savefig(f"outputs/{metric}_{stat}_top_10_over_time_yearly.png")
        plt.show()
