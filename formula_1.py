import pandas as pd
import matplotlib.pyplot as plt


drivers_df = pd.read_csv('csv/drivers.csv')
races_df = pd.read_csv('csv/races.csv')
results_df = pd.read_csv('csv/results.csv')
lap_times_df = pd.read_csv('csv/lap_times.csv')
driver_standings_df = pd.read_csv('csv/driver_standings.csv')
circuits_df = pd.read_csv('csv/circuits.csv')

#  Driver with the most points in descending order
most_points_df = driver_standings_df.sort_values(by='points', ascending=False).drop_duplicates(['driverId'])
most_points_df = most_points_df.merge(drivers_df, on='driverId', how='left')[['surname', 'points']]
most_points_df.to_csv('most_points_drivers.csv', index=False)

# Driver who won the most races
winners_df = results_df[results_df['positionOrder'] == 1]
win_count_df = winners_df['driverId'].value_counts().reset_index()
win_count_df.columns = ['driverId', 'wins']
win_count_df = win_count_df.merge(drivers_df, on='driverId', how='left')[['surname', 'wins']]
win_count_df.to_csv('most_wins_drivers.csv', index=False)

#fastest lap on the Monza 
monza_circuit_id = circuits_df[circuits_df['name'].str.contains("Monza")]['circuitId'].iloc[0]
monza_races_ids = races_df[races_df['circuitId'] == monza_circuit_id]['raceId']
fastest_lap_df = lap_times_df[lap_times_df['raceId'].isin(monza_races_ids)].sort_values(by='milliseconds', ascending=True).head(1)
fastest_lap_df = fastest_lap_df.merge(drivers_df, on='driverId', how='left')[['surname', 'milliseconds']]
fastest_lap_df.to_csv('fastest_lap_monza_driver.csv', index=False)

# Visualization example: Number of Wins per Driver (Top 10 for simplicity)
top_win_count_df = win_count_df.sort_values('wins', ascending=False).head(10)
plt.figure(figsize=(10, 8))
plt.barh(top_win_count_df['surname'], top_win_count_df['wins'])
plt.xlabel('Number of Wins')
plt.ylabel('Driver')
plt.title('Top 10 Drivers by Number of Wins')
plt.tight_layout()
plt.savefig('top_drivers_by_wins.png')
plt.show()
