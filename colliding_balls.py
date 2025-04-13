import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib

# Set FFmpeg path explicitly
matplotlib.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'  # Adjust the path if needed



# Parameters
num_balls = 100
radius = 1.0
box_size = 100
max_velocity = 3



# Initialize ball positions and velocities
positions = np.random.rand(num_balls, 2) * (box_size - 2 * radius) + radius
velocities = (np.random.rand(num_balls, 2) - 0.5) * max_velocity



# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_aspect('equal')


# Scatter plot for the balls
balls = ax.scatter(positions[:, 0], positions[:, 1], s=100, color='blue')



# Update function for the simulation
def update(frame):
    global positions, velocities

    # Move balls based on velocities
    positions += velocities

    # Wall collisions
    for i in range(num_balls):
        if positions[i, 0] <= radius or positions[i, 0] >= box_size - radius:
            velocities[i, 0] = -velocities[i, 0]
        if positions[i, 1] <= radius or positions[i, 1] >= box_size - radius:
            velocities[i, 1] = -velocities[i, 1]

    # Ball–ball collisions: flip both velocities if too close
    for i in range(num_balls):
        for j in range(i + 1, num_balls):
            delta = positions[i] - positions[j]
            dist = np.linalg.norm(delta)
            if dist <= 2 * radius:
                velocities[i,0] = -velocities[i,0]
                velocities[i,1] = -velocities[i,1]
                velocities[j,0] = -velocities[j,0]
                velocities[j,1] = -velocities[j,1]

    # Update plot
    balls.set_offsets(positions)
    return balls,




# Create the animation
ani = FuncAnimation(fig, update, frames=400, interval=50, blit=True)

# Specify the writer (FFMpegWriter) and save the animation
writer = FFMpegWriter(fps=30, metadata=dict(artist='Me', title='Balls Animation'))
ani.save('balls_animation.mp4', writer=writer)

# Display the animation
plt.show()
