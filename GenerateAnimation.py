import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import stats

# Load the data
df = pd.read_csv('data.csv')

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Sort the data by Date to ensure oldest points are first
df = df.sort_values(by='Date').reset_index(drop=True)  # Ensure data is in chronological order

# Create the figure and axis
fig, ax = plt.subplots(figsize=(19.2, 10.8))
ax.set_xlim(df['Date'].min(), df['Date'].max())
ax.set_ylim(df['Consumption'].min() - 1, df['Consumption'].max() + 1)
ax.set_ylabel('Consumption (L/100km)')
ax.grid(True)

# Initialize empty lists for data points and the line
xdata, ydata = [], []
# Updated to use a red dotted line with markers
ln, = ax.plot([], [], color='red', linestyle=':', marker='o', label='Fuelings')
trendline, = ax.plot([], [], 'b-', label='Trendline', linewidth=3)  # Blue trendline

# List to store text annotations
text_annotations = []

# Animation frame rate (frames per second)
fps = int(sys.argv[1])  # Adjust this to control the speed of the animation

# Duration to display text annotations (in seconds)
text_display_duration = 1/fps  # Display text based on the fps value

# Calculate the number of frames to display the text
frames_to_display_text = int(fps * text_display_duration)

# Function to initialize the animation
def init():
    ln.set_data([], [])
    trendline.set_data([], [])
    return ln, trendline

# Function to update the animation
def update(frame):
    # Append new data point (left to right)
    xdata.append(df['Date'][frame])
    ydata.append(df['Consumption'][frame])
    ln.set_data(xdata, ydata)
    
    # Calculate the trendline
    if len(xdata) > 1:
        # Convert dates to numeric values for trendline calculation
        x_num = np.arange(len(xdata))  # Use frame count as x-axis for trendline calculation
        slope, intercept, _, _, _ = stats.linregress(x_num, ydata)
        trendline.set_data(xdata, slope * x_num + intercept)
    
    # Add a text annotation for the current consumption value
    text = ax.annotate(
    f'{df["Consumption"][frame]:.2f}',
    xy=(df['Date'][frame], df['Consumption'][frame]),
    xytext=(15, 5),               # 15 pixels to the right and 5 pixels up
    textcoords='offset points',  # Interpret xytext as an offset in points
    fontsize=9,
    color='black',
    ha='center',
    va='bottom'
)
    text_annotations.append((frame, text))  # Store the frame number and text object
    
    # Remove text annotations that have been displayed for the desired duration
    current_frame = frame
    while len(text_annotations) > 0 and current_frame - text_annotations[0][0] >= frames_to_display_text:
        text_annotations.pop(0)[1].remove()  # Remove the oldest annotation
    
    # Update the Odometer legend at the top
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, title=f'Odometer: {df["Odometer"][frame]:.0f}')
    
    return ln, trendline, *[text for (_, text) in text_annotations]

# Create the animation
ani = FuncAnimation(fig, update, frames=range(len(df)), init_func=init, blit=True)

# Save the animation
ani.save('output.mp4', writer='ffmpeg', fps=fps)