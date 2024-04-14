# GravityGame
A WIP pygame-based gravity-simulation golf game.

# Background

We start with Newton's Law of Gravitation, and set it equal to Netwon's second law

$F = \frac{GMm}{r^2} = ma = m\frac{{\Delta}v}{t}$

Where $F$ is gravitational force, $G$ is the gravitational constant, $M$ and $m$ are the masses of the two interacting objects, $r$ is the CENTER TO CENTER separation and $a$ is the acceleration due to gravity. 

This can be rearranged as:

${\Delta}v = \frac{GMt}{r^2}$

${\Delta}v$ is the change in velocity of a $m$ due to an external mass $M$

![alt text](VelocityDiagram.png)

By summing all of the ${\Delta}v$ terms for each mass $M$, we can get the net velocity (as above). From which, we can get the distance travelled by the pointmass $m$ in a timestep $t$

$d=v{\cdot}t$

#Gif Demos
Note: The gifs are recorded at a very low framerate. The program maintains a steady 60fps at these object numbers.

![alt text](Demo.gif)

![alt text](Demo2.gif)
