"""
Flight Delay Analytics and Reporting
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_analytics():
    """Generate detailed analytics datasets"""
    
    # Load flight data
    df = pd.read_csv('/home/ubuntu/flight_delay_data.csv')
    
    # 1. Delay Statistics
    delay_stats = pd.DataFrame({
        'Metric': ['Mean Delay', 'Median Delay', 'Std Dev', 'Min Delay', 'Max Delay', 'Delayed Flights %'],
        'Value': [
            df['Delay_Minutes'].mean(),
            df['Delay_Minutes'].median(),
            df['Delay_Minutes'].std(),
            df['Delay_Minutes'].min(),
            df['Delay_Minutes'].max(),
            (df['Is_Delayed'].sum() / len(df)) * 100
        ]
    })
    delay_stats.to_csv('/home/ubuntu/flight_delay_statistics.csv', index=False)
    
    # 2. Hourly Analysis
    hourly_analysis = df.groupby('Departure_Hour').agg({
        'Delay_Minutes': ['mean', 'count', 'std'],
        'Is_Delayed': 'sum'
    }).round(2)
    hourly_analysis.columns = ['Avg_Delay', 'Flight_Count', 'Std_Dev', 'Delayed_Count']
    hourly_analysis.to_csv('/home/ubuntu/flight_hourly_analysis.csv')
    
    # 3. Weather Impact Analysis
    weather_impact = pd.DataFrame({
        'Weather_Factor': ['Temperature', 'Humidity', 'Wind_Speed', 'Visibility', 'Precipitation'],
        'Correlation_with_Delay': [
            df['Temperature'].corr(df['Delay_Minutes']),
            df['Humidity'].corr(df['Delay_Minutes']),
            df['Wind_Speed'].corr(df['Delay_Minutes']),
            df['Visibility'].corr(df['Delay_Minutes']),
            df['Precipitation'].corr(df['Delay_Minutes'])
        ]
    }).round(3)
    weather_impact.to_csv('/home/ubuntu/flight_weather_impact.csv', index=False)
    
    # 4. Route Analysis
    route_analysis = pd.DataFrame({
        'Route_Distance_Range': ['0-500km', '500-1500km', '1500-3000km', '3000-5000km'],
        'Avg_Delay': [
            df[df['Route_Distance'] <= 500]['Delay_Minutes'].mean(),
            df[(df['Route_Distance'] > 500) & (df['Route_Distance'] <= 1500)]['Delay_Minutes'].mean(),
            df[(df['Route_Distance'] > 1500) & (df['Route_Distance'] <= 3000)]['Delay_Minutes'].mean(),
            df[df['Route_Distance'] > 3000]['Delay_Minutes'].mean()
        ],
        'Flight_Count': [
            len(df[df['Route_Distance'] <= 500]),
            len(df[(df['Route_Distance'] > 500) & (df['Route_Distance'] <= 1500)]),
            len(df[(df['Route_Distance'] > 1500) & (df['Route_Distance'] <= 3000)]),
            len(df[df['Route_Distance'] > 3000])
        ]
    }).round(2)
    route_analysis.to_csv('/home/ubuntu/flight_route_analysis.csv', index=False)
    
    # 5. Airline Performance
    airline_perf = pd.DataFrame({
        'Performance_Range': ['70-80%', '80-85%', '85-90%', '90-95%', '95-99%'],
        'Avg_Delay': [
            df[(df['Airline_Performance'] >= 70) & (df['Airline_Performance'] < 80)]['Delay_Minutes'].mean(),
            df[(df['Airline_Performance'] >= 80) & (df['Airline_Performance'] < 85)]['Delay_Minutes'].mean(),
            df[(df['Airline_Performance'] >= 85) & (df['Airline_Performance'] < 90)]['Delay_Minutes'].mean(),
            df[(df['Airline_Performance'] >= 90) & (df['Airline_Performance'] < 95)]['Delay_Minutes'].mean(),
            df[(df['Airline_Performance'] >= 95) & (df['Airline_Performance'] <= 99)]['Delay_Minutes'].mean()
        ],
        'Flight_Count': [
            len(df[(df['Airline_Performance'] >= 70) & (df['Airline_Performance'] < 80)]),
            len(df[(df['Airline_Performance'] >= 80) & (df['Airline_Performance'] < 85)]),
            len(df[(df['Airline_Performance'] >= 85) & (df['Airline_Performance'] < 90)]),
            len(df[(df['Airline_Performance'] >= 90) & (df['Airline_Performance'] < 95)]),
            len(df[(df['Airline_Performance'] >= 95) & (df['Airline_Performance'] <= 99)])
        ]
    }).round(2)
    airline_perf.to_csv('/home/ubuntu/flight_airline_performance.csv', index=False)
    
    # 6. Congestion Impact
    congestion_bins = pd.cut(df['Airport_Congestion'], bins=5)
    congestion_analysis = df.groupby(congestion_bins).agg({
        'Delay_Minutes': ['mean', 'count'],
        'Is_Delayed': 'sum'
    }).round(2)
    congestion_analysis.columns = ['Avg_Delay', 'Flight_Count', 'Delayed_Count']
    congestion_analysis.to_csv('/home/ubuntu/flight_congestion_analysis.csv')
    
    print("Analytics generated successfully!")
    print("\nDelay Statistics:")
    print(delay_stats)
    print("\nWeather Impact:")
    print(weather_impact)
    print("\nRoute Analysis:")
    print(route_analysis)

if __name__ == "__main__":
    generate_analytics()
