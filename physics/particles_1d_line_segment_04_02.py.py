# -------------------------------------------------------------------
# particles_1d_line_segment_04_02.py
#
# Finds equilibrium state of distributed particles
#
# Particle System:
#   - Dimensions                :   1D
#   - Constraint type           :   Line Segment
#   - Number of particles       :   4
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

# Plot settings
PLOT_HEIGHT = 2
PLOT_WIDTH = (PARTICLE_RIGHT_POSITION + 1) - (PARTICLE_LEFT_POSITION - 1)

# Interaction force law
IS_REPULSIVE = True
FORCE_DECAY_POWER = 1
FORCE_POSITION_GAIN = 0.03

direction = -1
if IS_REPULSIVE:
    direction = 1


class Particle:
    """Particle Class"""

    def __init__(self, position, name, color):
        self.position = position
        self.name = name
        self.color = color
        self.total_force = 0
        pass

    def compute_force(self, mate_particle, direction, FORCE_DECAY):
        dx = self.position - mate_particle.position
        if not dx == 0:
            force = direction * np.sign(dx)/(np.abs(dx)**FORCE_DECAY)
        else:
            force = 0  # In case of singularity, ignore the force.

        self.total_force += force

    def move(self, gain):
        self.position = self.position + gain * self.total_force


def update_graphics(frame):
    """
    Runs the simulaiton and updates the graphics

    Parameters
    ----------
    frame : frame number
    
    Returns
    -------
    particles_marker : A plot axis handler for ploting the particles
    text_time_step : A plot axis handler for printing time steps
    particlet_1_text : A plot axis handler for printing particle 1 location
    particlet_2_text : A plot axis handler for printing particle 2 location
    """
    global particles

    time_step = frame + 3  # FuncAnimation() is 3 steps ahread

    poss = []
    for particle in particles:

        particle.total_force = 0
        particle.compute_force(particle_L, direction, FORCE_DECAY_POWER)
        particle.compute_force(particle_R, direction, FORCE_DECAY_POWER)

        for mate_particle in particles:
            if not mate_particle == particle:
                particle.compute_force(
                    mate_particle, direction, FORCE_DECAY_POWER)

        particle.move(FORCE_POSITION_GAIN)
        poss.append(particle.position)

    np_particles = np.array(poss)

    particles_marker.set_data([np_particles, np_particles*0 + PLOT_HEIGHT/2])

    particlet_1_text.set_x(poss[0])
    particlet_2_text.set_x(poss[1])

    particlet_1_text.set_text('{:.2f}'.format(poss[0]))
    particlet_2_text.set_text('{:.2f}'.format(poss[1]))

    text_time_step.set_text('Time step: {}'.format(time_step))

    return particles_marker, text_time_step, particlet_1_text, particlet_2_text


# ----------------
# Define particles
# ----------------
particle_L = Particle(PARTICLE_LEFT_POSITION, 'L', 'k')
particle_R = Particle(PARTICLE_RIGHT_POSITION, 'R', 'k')
particle_1 = Particle(1.00, '1', 'ro')
particle_2 = Particle(2.00, '2', 'go')
particles = [particle_1, particle_2]

# --------------
# Plot particles
# --------------
fig, ax = plt.subplots(figsize=(PLOT_WIDTH+1, PLOT_HEIGHT+1))
ax.grid()
ax.set_yticklabels([])

ax.set(aspect='equal',
       xlim=(PARTICLE_LEFT_POSITION-1, PARTICLE_RIGHT_POSITION+1),
       ylim=(0, PLOT_HEIGHT), xlabel='x')

ax.plot([PARTICLE_LEFT_POSITION, PARTICLE_RIGHT_POSITION],
        [PLOT_HEIGHT/2, PLOT_HEIGHT/2], 'o-')

particles_marker, = ax.plot([], [], 'o')  # 'r*'

particlet_1_text = ax.text(
    particles[0].position, PLOT_HEIGHT/2+0.25, '{:.2f}'.format(particles[0].position))
particlet_2_text = ax.text(
    particles[1].position, PLOT_HEIGHT/2+0.25, '{:.2f}'.format(particles[1].position))

# ----------------
# Plot information
# ----------------
ax_info = fig.add_axes([0.12, 0.01, 0.78, 0.06])
ax_info.axis("off")
text_time_step = ax_info.text(0, 0.25, 'Time step: {}'.format(0))

# ---------
# Animation
# ---------
ani = FuncAnimation(fig, update_graphics, interval=20,
                    blit=True, repeat=False, frames=300)

# ani.save('physics/animation_' + os.path.basename(__file__).split('.')
#          [0] + '_' + str(int(time.time())) + '.mp4', fps=20)

plt.show()
