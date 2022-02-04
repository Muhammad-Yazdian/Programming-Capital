# -------------------------------------------------------------------
# particles_1d_line_segment_03_02.py
#
# Finds equilibrium state of distributed particles
#
# Particle System:
#   - Dimensions                :   1D
#   - Constraint type           :   Line Segment
#   - Number of particles       :   3
#   - Number of pixed particles :   2
#
# (C) 2021 Seied Muhammad Yazdian, Zurich, Switzerland
# Released under GNU Public License (GPL)
# https://github.com/Muhammad-Yazdian
# -------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.animation import FuncAnimation
import time
import os 

# Particle Settings
PARTICLE_LEFT_POSITION = 0
PARTICLE_RIGHT_POSITION = 6
particle_free_position = 1

# Plot settings
PLOT_HEIGHT = 2
PLOT_WIDTH = (PARTICLE_RIGHT_POSITION + 1) - (PARTICLE_LEFT_POSITION - 1)

# Interaction force law
IS_REPULSIVE = True
FORCE_DECAY_POWER = 1
FORCE_POSITION_GAIN = 0.1

direction = -1
if IS_REPULSIVE:
    direction = 1


def update_graphics(frame):
    """
    Runs the simulaiton and updates the graphics

    Parameters
    ----------
    frame : frame number
    
    Returns
    -------
    point_1, : A plot axis handler for ploting the particle
    text_1 : A plot axis handler for printing the particle location
    text_time_step : A plot axis handler for printing time steps
    """
    global particle_free_position

    time_step = frame + 3 # FuncAnimation() is 3 steps ahread
    
    dx = particle_free_position - PARTICLE_LEFT_POSITION
    if not dx == 0:
        force_left_particle = direction * np.sign(
            dx)/(np.abs(dx)**FORCE_DECAY_POWER)
    else:
        force_left_particle = 0  # In case of singularity, ignore the force.

    dx = particle_free_position - PARTICLE_RIGHT_POSITION
    if not dx == 0:
        force_right_particle = direction * np.sign(
            dx)/(np.abs(dx)**FORCE_DECAY_POWER)
    else:
        force_right_particle = 0  # In case of singularity, ignore the force.

    particle_free_position = particle_free_position + \
        FORCE_POSITION_GAIN * (force_left_particle + force_right_particle)

    point_1.set_data([particle_free_position, PLOT_HEIGHT/2])
    text_1.set_x(particle_free_position)
    text_1.set_text('{:.2f}'.format(particle_free_position))
    text_time_step.set_text('Time step: {}'.format(time_step))

    return point_1, text_1, text_time_step


# Plot the particles
fig, ax = plt.subplots(figsize=(PLOT_WIDTH+1, PLOT_HEIGHT+1))
ax.grid()
ax.set_yticklabels([])
ax.set(aspect='equal',
       xlim=(PARTICLE_LEFT_POSITION-1, PARTICLE_RIGHT_POSITION+1),
       ylim=(0, PLOT_HEIGHT), xlabel='x')
ax.plot([PARTICLE_LEFT_POSITION, PARTICLE_RIGHT_POSITION],
        [PLOT_HEIGHT/2, PLOT_HEIGHT/2], 'o-')
point_1, = ax.plot(particle_free_position, PLOT_HEIGHT/2, 'o')
text_1 = ax.text(particle_free_position, PLOT_HEIGHT/2+0.25,
                 '{:.2f}'.format(particle_free_position))

ax_info = fig.add_axes([0.12, 0.01, 0.78, 0.06])
ax_info.axis("off")
text_time_step = ax_info.text(0, 0.25, 'Time step: {}'.format(0))

ani = FuncAnimation(fig, update_graphics, interval=20,
                    blit=True, repeat=False, frames=300)

# ani.save('physics/animation_' + os.path.basename(__file__).split('.')
#          [0] + '_' + str(int(time.time())) + '.mp4', fps=20)

plt.show()