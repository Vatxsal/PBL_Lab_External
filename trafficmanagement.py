import numpy as np
import pandas as pd
import time
import random

# Load real-time traffic data from the CSV file
def load_real_time_data(filename="real_time_traffic1.csv"):
    df = pd.read_csv(filename)
    return df

# Adjust traffic signal durations based on traffic density
def adjust_traffic_signals(df):
    """
    Adjusts the traffic signal durations based on the traffic density.
    The higher the traffic density, the longer the green light duration.
    
    Parameters:
    - df: DataFrame containing the traffic density and signal information
    
    Returns:
    - DataFrame with adjusted traffic signal durations
    """
    for i, row in df.iterrows():
        # Calculate a scaling factor based on traffic density
        scaling_factor = row['traffic_density'] / 500  # Assume max density is 500
        
        # Increase the green light duration proportionally to the traffic density
        df.at[i, 'green_light_duration'] = min(90, max(30, row['green_light_duration'] * scaling_factor))
        
        # Reducing red light duration if green duration increases (to keep total cycle time balanced)
        df.at[i, 'red_light_duration'] = 120 - df.at[i, 'green_light_duration']
        
    return df

# Simulate traffic diversion if a particular intersection's traffic is too high
def traffic_diversion(df, threshold=400):
    """
    Diverts traffic from intersections with high traffic density to less congested intersections.
    
    Parameters:
    - df: DataFrame containing traffic density at intersections
    - threshold: Traffic density threshold for diversion
    
    Returns:
    - Updated DataFrame with adjusted traffic densities
    """
    # Identify intersections with traffic density above the threshold
    high_traffic_intersections = df[df['traffic_density'] > threshold]
    
    for i, row in high_traffic_intersections.iterrows():
        # Find the intersection with the lowest traffic density
        least_traffic_index = df['traffic_density'].idxmin()
        
        if least_traffic_index != i:  # Only divert if there's another intersection with less traffic
            diverted_traffic = random.randint(20, 50)  # Amount of traffic to divert
            df.at[i, 'traffic_density'] -= diverted_traffic
            df.at[least_traffic_index, 'traffic_density'] += diverted_traffic
            print(f"Diverting {diverted_traffic} vehicles from {row['intersection_id']} to {df.loc[least_traffic_index, 'intersection_id']}")
    
    return df

# Traffic signal cycle simulation (real-time simulation)
def simulate_traffic_cycle(df):
    """
    Simulate the traffic signal cycles based on the traffic data.
    
    Parameters:
    - df: DataFrame with the adjusted traffic signal information
    
    Simulates the traffic signal cycle for each intersection (green, yellow, red light).
    """
    while True:
        for i, row in df.iterrows():
            print(f"\n{row['intersection_id']} Traffic Signal Cycle:")
            print(f"  Green Light Duration: {row['green_light_duration']} seconds")
            print(f"  Yellow Light Duration: {row['yellow_light_duration']} seconds")
            print(f"  Red Light Duration: {row['red_light_duration']} seconds")
            
            # Simulate traffic light cycle (in real life, these would control physical lights)
            print(f"  {row['intersection_id']} Green Light ON")
            time.sleep(row['green_light_duration'])
            print(f"  {row['intersection_id']} Yellow Light ON")
            time.sleep(row['yellow_light_duration'])
            print(f"  {row['intersection_id']} Red Light ON")
            time.sleep(row['red_light_duration'])
def save_traffic_data_to_csv(df, filename="final_traffic_density.csv"):
    """
    Save the traffic data to a CSV file.
    
    Parameters:
    - df: DataFrame containing the traffic data
    - filename: Name of the file where the data will be saved
    
    Returns:
    - None
    """
    df.to_csv(filename, index=False)
    print(f"Traffic data saved to {filename}")

# Traffic Management System main function
def main():
    # Load the real-time traffic data (we'll assume the data is already generated)
    df = load_real_time_data()

    # Print the initial traffic data
    print("Initial Traffic Data:")
    print(df)
    
    # Adjust the signal durations based on traffic density
    df = adjust_traffic_signals(df)
    
    # Print the adjusted traffic signal durations
    print("\nAdjusted Traffic Signals based on Traffic Density:")
    print(df)
    
    # Simulate traffic diversion if needed
    df = traffic_diversion(df, threshold=400)
    
    # Print the updated traffic data after diversion
    print("\nTraffic Data After Diversion:")
    print(df)
    
    save_traffic_data_to_csv(df)
   
    # Simulate the traffic signal cycles
    print("\nSimulating Traffic Signal Cycles...")
    simulate_traffic_cycle(df)

# Run the traffic management system
if __name__ == "__main__":
    main()
