# Ring for stator
# Helix for coil
# Box for battery / power source

from vpython import *
from math import sin, cos, pi, atan2

# Setup
scene = canvas(title="Electric Motors",
               width=900,
               height=650,
               background=color.white)

scene.forward = vector(0, 0, -1)
scene.range = 4

# Stator ring
stator = ring(pos=vector(0, 0, 0),
              axis=vector(0, 0, 1),
              radius=2,
              thickness=0.07,
              color=color.gray(0.6))

# Axle through the motor
axle = cylinder(pos=vector(0, 0, -0.7),
                axis=vector(0, 0, 1.4),
                radius=0.06,
                color=color.black)

# Rotor bar
rotor_bar = box(pos=vector(0, 0, 0),
                size=vector(2.4, 0.18, 0.18),
                color=color.red)

# Coil/helix on the rotor
coil = helix(pos=vector(-0.65, 0, 0),
             axis=vector(1.3, 0, 0),
             radius=0.22,
             thickness=0.035,
             coils=10,
             color=color.orange)

# Rotating magnetic field arrow
field_arrow = arrow(pos=vector(0, 0, 0),
                    axis=vector(1.8, 0, 0),
                    shaftwidth=0.07,
                    color=color.blue)

# Power source / battery box
battery = box(pos=vector(-3, 1.8, 0),
              size=vector(0.9, 0.5, 0.4),
              color=color.purple)

# Battery label
battery_label = label(pos=vector(-3, 2.25, 0),
                      text="AC Power",
                      height=14,
                      box=False,
                      color=color.black)

# Positive battery label
plus_label = label(pos=vector(-2.65, 1.8, 0),
                   text="+",
                   height=18,
                   box=False,
                   color=color.black)

# Negative battery label
minus_label = label(pos=vector(-3.35, 1.8, 0),
                    text="-",
                    height=18,
                    box=False,
                    color=color.black)

# Wire from battery to motor
wire1 = curve(pos=[vector(-2.55, 1.8, 0),
                   vector(-1.7, 1.2, 0),
                   vector(-1.2, 0.7, 0)],
              radius=0.025,
              color=color.black)

# Second wire from battery to motor
wire2 = curve(pos=[vector(-3.45, 1.8, 0),
                   vector(-1.9, -1.2, 0),
                   vector(-1.2, -0.7, 0)],
              radius=0.025,
              color=color.black)

# Info label
info = label(pos=vector(0, -2.8, 0),
             text="",
             height=14,
             box=False,
             color=color.black)

# Physics parameters (All numbers arbitrary right now. Make them sliders and such.)
V = 12.0              # Voltage
R = 3.0               # Resistance
k_back = 0.50         # Back EMF constant
k_t = 0.50            # Torque constant
J = 0.05              # Moment of inertia

frequency = 0.8       # AC frequency
omega_drive = 2 * pi * frequency   # Angular speed of rotating magnetic field

# Initial conditions (Also arbitrary. Change.)
theta = 0.2
omega = 0.0

t = 0.0
dt = 0.002

# Keeps an angle between -pi and pi
def wrap_angle(angle):
    return atan2(sin(angle), cos(angle))

# Calculates the rotor's angular velocity and angular acceleration
def derivatives(theta, omega, t):
    field_angle = omega_drive * t

    delta = wrap_angle(field_angle - theta)

    back_emf = k_back * omega

    current = (V - back_emf) / R

    torque = k_t * current * sin(delta)

    alpha = torque / J

    return omega, alpha

# Uses the fourth-order Runge-Kutta method to update theta and omega
def rk4_step(theta, omega, t, dt):
    k1_theta, k1_omega = derivatives(theta, omega, t)

    k2_theta, k2_omega = derivatives(
        theta + 0.5 * dt * k1_theta,
        omega + 0.5 * dt * k1_omega,
        t + 0.5 * dt
    )

    k3_theta, k3_omega = derivatives(
        theta + 0.5 * dt * k2_theta,
        omega + 0.5 * dt * k2_omega,
        t + 0.5 * dt
    )

    k4_theta, k4_omega = derivatives(
        theta + dt * k3_theta,
        omega + dt * k3_omega,
        t + dt
    )

    new_theta = theta + (dt / 6) * (
        k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta
    )

    new_omega = omega + (dt / 6) * (
        k1_omega + 2 * k2_omega + 2 * k3_omega + k4_omega
    )

    return new_theta, new_omega

# Updates the visual rotor bar and coil so they rotate together
def update_rotor_visuals(theta):
    direction = vector(cos(theta), sin(theta), 0)

    rotor_length = 2.4
    rotor_bar.axis = rotor_length * direction
    rotor_bar.up = vector(-sin(theta), cos(theta), 0)

    coil_length = 1.3
    coil.pos = -(coil_length / 2) * direction
    coil.axis = coil_length * direction

# Main animation loop
while True:
    rate(250)

    theta, omega = rk4_step(theta, omega, t, dt)

    field_angle = omega_drive * t

    stator_radius = 2
    field_arrow_length = 1.8
    field_arrow.axis = field_arrow_length * vector(cos(field_angle), sin(field_angle), 0)

    update_rotor_visuals(theta)

    back_emf = k_back * omega
    current = (V - back_emf) / R

    info.text = "Rotor speed: " + str(round(omega, 2)) + " rad/s\n" + \
                "Back EMF: " + str(round(back_emf, 2)) + " V\n" + \
                "Current: " + str(round(current, 2)) + " A"

    t += dt