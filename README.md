# GravityGame
A WIP pygame-based gravity-simulation golf game.

# Background

We start with Newton's Law of Gravitation, and set it equal to Netwon's second law

$F = \frac{GMm}{r^2} = ma = m\frac{{\Delta}v}{t}$

Where $F$ is gravitational force, $G=6{\cdot}10^{-11}$ is the gravitational constant, $M$ and $m$ are the masses of the two interacting objects, $r$ is the CENTER TO CENTER separation and $a$ is the acceleration due to gravity. 

This can be rearranged as:

${\Delta}v = \frac{GMt}{r^2}$

${\Delta}v$ is the change in velocity of a $m$ due to an external mass $M$

![alt text](VelocityDiagram.png)

By summing all of the ${\Delta}v$ terms for each mass $M$, we can get the net velocity (his is equivalent to calculating the net force). From which, we can get the distance travelled by the pointmass $m$ in a timestep $t$:

$d=v{\cdot}t$

The smaller the time-step, the more accurate the simulations. However, a scaling factor of ~3e6x speed was used as a real-time gravity simulation is not very entertaining. 

# Gif Demos

Note: The gifs are recorded at a very low framerate. The program maintains a steady 60fps at these object numbers.

This demo is of the "Sandbox mode" - placing the planets manually
![Sandbox Gif](Demo.gif)

This next demo is of two Earths orbiting the Sun. Masses, velocities and separations are all accurate.
![Binary Earth Orbit](Demo2.gif)

This next demo is of random point-masses at random locations, showing off the time-scale feature.
![Randomly Generated Point w/ Time Scale Change](Demo3.gif)
