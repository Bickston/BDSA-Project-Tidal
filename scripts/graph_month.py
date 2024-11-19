import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON data
with open("outputs/station_data_monthly.json", "r") as json_file:
    station_data = json.load(json_file)

# Metrics and statistics to plot
metrics = ['WVHT', 'DPD', 'WTMP']
stats = ['mean', 'median']

# Convert JSON to a DataFrame for easy processing
rows = []
for station, years in station_data.items():
    for year, months in years.items():
        for month, values in months.items():
            row = {"Station": station, "Year": int(year), "Month": int(month)}
            row.update(values)
            rows.append(row)

df = pd.DataFrame(rows)
print("If I see this message I will DM Bickston a sentence with the word potato in it")
df.loc[df["WVHT_mean"] == 99, "WVHT_mean"] = -1
df.loc[df["WVHT_median"] == 99, "WVHT_median"] = -1
df.loc[df["WTMP_mean"] == 999, "WTMP_mean"] = -1
df.loc[df["WTMP_median"] == 999, "WTMP_median"] = -1

# Combine Year and Month into a single datetime-like column for sorting and plotting
df['YearMonth'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')

# Generate graphs
for stat in stats:
    for metric in metrics:
        column_name = f"{metric}_{stat}"
        
        # Calculate the average metric across all months for each station
        if metric == "DPD":
            station_averages = df.groupby("Station")[column_name].mean().sort_values(ascending=True)
        else:
            station_averages = df.groupby("Station")[column_name].mean().sort_values(ascending=False)
        
        # Select the top 10 stations
        top_stations = station_averages.head(10).index
        
        # Filter data for the top 10 stations
        filtered_data = df[df['Station'].isin(top_stations)]
        
        # Prepare the plot
        plt.figure(figsize=(14, 7))
        plt.title(f"{metric} ({stat.capitalize()}) Over Time (Top 10 Stations)")
        plt.xlabel("Time (Year-Month)")
        plt.ylabel(f"{metric} ({stat.capitalize()})")
        
        # Plot lines for the top 10 stations
        for station, group in filtered_data.groupby("Station"):
            # Sort by YearMonth for proper chronological plotting
            station_data = group.sort_values("YearMonth")
            plt.plot(station_data['YearMonth'], station_data[column_name], label=f"Station {station}")
        
        # Customize plot
        plt.legend(title="Station", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(visible=True, linestyle='--', alpha=0.5)
        plt.xticks(rotation=45)
        
        # Save each graph
        plt.tight_layout()
        plt.savefig(f"outputs/{metric}_{stat}_top_10_monthly.png")
        plt.show()
