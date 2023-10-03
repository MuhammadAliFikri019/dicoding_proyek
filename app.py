
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Set the style to 'dark' for Seaborn
sns.set(style='dark')

# Define function to create daily rents DataFrame
def create_daily_rents_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    df.set_index('dteday', inplace=True)

    daily_rents_df = df.resample(rule='D').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum",
    })
    daily_rents_df.reset_index(inplace=True)
    daily_rents_df.rename(columns={
        "cnt": "total_cnt",
    }, inplace=True)
    
    return daily_rents_df

# Load the data
all_df = pd.read_csv("all_data.csv")

# Define datetime columns and sort the DataFrame
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Define minimum and maximum dates
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Create a Streamlit sidebar with logo and date input
with st.sidebar:
    # Add the company logo
    st.image("https://raw.githubusercontent.com/MuhammadAliFikri019/desktop-tutorial/26f0ecc3fffe0efca3d76c0b08016448ec601f3d/Group%2020%20(2).png")
    
    # Get start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the main DataFrame based on the selected date range
main_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

# Create the Daily rents DataFrame
daily_rents_df = create_daily_rents_df(main_df)

# Display the header with company name
st.markdown("""
    <div style='text-align: center;'>
        <h1>Dicoding Student</h1>
        <h1>Muhammad Ali Fikri Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Add subheaders and metrics in three columns layout
st.subheader('Daily Rents')

# Create a layout with three columns
col1, col2, col3 = st.columns(3)

# In the first column
with col1:
    total_rents = daily_rents_df.total_cnt.sum()
    st.metric("Total Rents", value=total_rents)

# In the second column
with col2:
    total_casual_user_rents = daily_rents_df.casual.sum()
    st.metric("Total Rents by Casual Users", value=total_casual_user_rents)

# In the third column
with col3:
    total_registered_user_rents = daily_rents_df.registered.sum()
    st.metric("Total Rents by Registered Users", value=total_registered_user_rents)

# Add subheaders and metrics in three columns layout
st.subheader("Daily Rents Plot")
# Create a Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(16, 8))

# Your plotting code here (e.g., creating a line plot)
plt.fill_between(
    daily_rents_df["dteday"],
    daily_rents_df["total_cnt"],
    alpha=0.5,
    color="#90CAF9",
    label='Total Rents'
)
plt.plot(
    daily_rents_df["dteday"],
    daily_rents_df["total_cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
plt.title("Daily Rents Over Time", fontsize=20)
plt.xlabel("Date", fontsize=15)
plt.ylabel("Total Rents", fontsize=15)
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Display the Matplotlib figure using st.pyplot()
st.pyplot(fig)

# Calculate the sum of 'cnt' for each season
season_counts = main_df.groupby('season')['cnt'].sum().reset_index()
season_counts['season'] = season_counts['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})


# Create a bar chart to show the sum of 'cnt' for each season with data labels
st.subheader("Total Rentals by Season")
fig, ax = plt.subplots(figsize=(10, 6))

# Create the bar chart to show the sum of 'cnt' for each season with data labels
sns.barplot(data=season_counts, x='season', y='cnt', palette='Blues', ax=ax)
ax.set_title("Total Rentals by Season", fontsize=16)
ax.set_xlabel("Season", fontsize=14)
ax.set_ylabel("Total Rentals", fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Add data labels above the bars with vertical padding
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=12, color='black', xytext=(0, 10),  # Adjust the padding here
                textcoords='offset points')

# Set the y-axis limit with padding
ax.set_ylim(top=ax.get_ylim()[1] * 1.2)

# Display the Matplotlib figure using st.pyplot()
st.pyplot(fig)

# Create a layout with four columns
col1, col2, col3, col4 = st.columns(4)

# Calculate the average temperature for the selected months
average_temp = main_df['temp'].mean()

# Format the average temperature as a string with degrees Celsius symbol
formatted_temp = f"{average_temp:.2f} °C"

# Display the average temperature using the st.metric widget in the first column
col1.metric(label="Average Temperature", value=formatted_temp, delta=None)

# Calculate the average atemp (feeling temperature) for the selected months
average_atemp = main_df['atemp'].mean()

# Format the average atemp as a string with degrees Celsius symbol
formatted_atemp = f"{average_atemp:.2f} °C"

# Display the average atemp using the st.metric widget in the second column
col2.metric(label="Average Feeling Temperature", value=formatted_atemp, delta=None)

# Calculate the average humidity for the selected months
average_humidity = main_df['hum'].mean()

# Format the average humidity as a percentage
formatted_humidity = f"{average_humidity:.2%}"

# Display the average humidity using the st.metric widget in the third column
col3.metric(label="Average Humidity", value=formatted_humidity, delta=None)

# Calculate the average windspeed for the selected months
average_windspeed = main_df['windspeed'].mean()

# Format the average windspeed as a decimal number
formatted_windspeed = f"{average_windspeed:.2f}"

# Display the average windspeed using the st.metric widget in the fourth column
col4.metric(label="Average Windspeed", value=formatted_windspeed, delta=None)

st.subheader("Seasonal Trend Analysis with Moving Average")

# Calculate the rolling mean (moving average) for a certain window size
rolling_window = 30  # Adjust the window size as needed
daily_rents_df['rolling_mean'] = daily_rents_df['total_cnt'].rolling(rolling_window).mean()

# Create a Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(16, 8))

# Plot the observed data
ax.plot(daily_rents_df["dteday"], daily_rents_df["total_cnt"], label='Observed', linewidth=2, color="#90CAF9")

# Plot the rolling mean as the trend
ax.plot(daily_rents_df["dteday"], daily_rents_df["rolling_mean"], label=f'Rolling Mean ({rolling_window}-day)', linewidth=2, color="orange")

# Set labels and title
ax.set_title("Daily Rents and Rolling Mean (Trend)", fontsize=20)
ax.set_xlabel("Date", fontsize=15)
ax.set_ylabel("Total Rents", fontsize=15)
ax.tick_params(axis='x', labelrotation=45)
ax.tick_params(axis='both', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

# Display the Matplotlib figure using st.pyplot()
st.pyplot(fig)
