# Ring for stator
# Helix for coil
# Box for battery / power source

from vpython import *
from math import sin, cos, pi, atan2, sqrt

# Setup
scene = canvas(title="Electric Motors",
               width=900,
               height=650,
               background=color.white)

scene.forward = vector(0, 0, -1)
scene.range = 5
scene.userzoom = False
scene.userspin = False

#Buttons

def toggle_zoom_out():
    scene.range += 1  # Zoom out
    if scene.range == 7:
        zoom_button_out.text = "Max Zoom"
        

def toggle_zoom_in():
    scene.range -= 1 #Zoom in
    if scene.range <= 2:
        scene.range -= 0.01
    if scene.range == 1:
        zoom_button_in.text = "Max Zoom"

zoom_button_out = button(  
    bind = toggle_zoom_out,
    text='Zoom Out', 
    color=color.black  
)
zoom_button_in = button(  
    bind = toggle_zoom_in,
    text='Zoom In', 
    color=color.black  
)

# Stator ring
stator = shapes.circle(radius=2, thickness=0.1)

# Make it 3D
extrusion(path=[vec(0,0,0), vec(0,0,0.1)],
          shape=stator,
          color=color.gray(0.5))

N = 20
l = 0.2

for i in range(3):
    thetaN=5*pi/12+i*pi/3
    thetaS=thetaN+pi
    offset = pi*0.08
    c = None
    if i == 0: c = color.red
    if i == 1: c = color.blue
    if i == 2: c = color.green
    magnetN = shapes.arc(radius=1.8, thickness=0.5, angle1=thetaN, angle2=thetaN+pi/6)
    magnetS = shapes.arc(radius=1.8, thickness=0.5, angle1=thetaS, angle2=thetaS+pi/6)
    extrusion(path=[vec(0, 0, 0,), vec(0, 0, 0.1)], shape=magnetN, color=color.gray(0.5))
    extrusion(path=[vec(0, 0, 0,), vec(0, 0, 0.1)], shape=magnetS, color=color.gray(0.5))
    coilN = helix(pos=1.3*vector(cos(thetaN+offset), sin(thetaN+offset), 0), axis=vector(cos(thetaN+pi/12), sin(thetaN+pi/12), 0), radius = 0.55, thickness=0.035, coils=N, length=l, color=c)
    coilS = helix(pos=1.3*vector(cos(thetaS+offset), sin(thetaS+offset), 0), axis=vector(cos(thetaS+pi/12), sin(thetaS+pi/12), 0), radius = 0.55, thickness=0.035, coils=N, length=l, color=c)

rmsV = 10
phase_impedance = 3.0
rmsI = rmsV / phase_impedance     # magnetic field created by current
mu0 = 4*pi*1e-7
frequency = 0.8
omega_electric = 2 * pi * frequency

poles = 2
omega_sync = 4 * pi * frequency / poles   # Mechanical synchronous speed for the rotating magnetic field

B_visual_scale = 1000   # Makes the magnetic field arrows visible on screen
t = 0

# Three-phase AC currents are 120 degrees apart
ac1 = rmsI*sqrt(2)*sin(omega_electric*t)
ac2 = rmsI*sqrt(2)*sin(omega_electric*t-2*pi/3)
ac3 = rmsI*sqrt(2)*sin(omega_electric*t-4*pi/3)
   
B1 = mu0*ac1*N/l*vector(cos(pi/2), sin(pi/2), 0)
B2 = mu0*ac2*N/l*vector(cos(pi/2+2*pi/3), sin(pi/2+2*pi/3), 0)
B3 = mu0*ac3*N/l*vector(cos(pi/2+4*pi/3), sin(pi/2+4*pi/3), 0)
B = B1+B2+B3

B1arrow = arrow(pos=vector(0, 0, 0), axis=B1*B_visual_scale, radius=0.06, color=color.red)
B2arrow = arrow(pos=vector(0, 0, 0), axis=B2*B_visual_scale, radius=0.06, color=color.green)
B3arrow = arrow(pos=vector(0, 0, 0), axis=B3*B_visual_scale, radius=0.06, color=color.blue)
Barrow = arrow(pos=vector(0, 0, 0), axis=B*B_visual_scale, radius=0.06, color=color.black)


# Axle through the motor
axle = cylinder(pos=vector(0, 0, -0.7),
                axis=vector(0, 0, 1.4),
                radius=0.06,
                color=color.black)

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

# Squirrel Cage Rotor
rotor_length = 1.4
rotor_radius = 0.9
num_bars = 6

# 1. Create Rotor Bars
rotor_bars = []
for i in range(num_bars):
    angle = i * ((2 * pi)/ num_bars) +pi/2
    bar_pos = vector(rotor_radius * cos(angle), rotor_radius * sin(angle), 0)
    bar = cylinder(pos=bar_pos - vector(0, 0, rotor_length/2), axis=vector(0, 0, rotor_length), radius=0.04, color=color.orange)
    rotor_bars.append(bar)

# 2. Create End Rings
end_ring_left = ring(pos=vector(0, 0, -rotor_length/2), axis=vector(0, 0, 1), radius=rotor_radius, thickness=0.06, color=color.orange)
end_ring_right = ring(pos=vector(0, 0, rotor_length/2), axis=vector(0, 0, 1), radius=rotor_radius, thickness=0.06, color=color.orange)

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

# EMF vs time graph
emf_graph = graph(title="Instantaneous Rotor EMF vs Time",
                  xtitle="Time (s)",
                  ytitle="Rotor EMF (V)",
                  width=500,
                  height=300, xmin=0, xmax = 10, scroll = True)

emf_curve = gcurve(graph=emf_graph, color=color.red)

# Torque vs time graph
torque_graph = graph(title="Torque vs Time",
                  xtitle="Time (s)",
                  ytitle="Torque (Nm)",
                  width=500,
                  height=300, xmin = 0, xmax = 10, scroll = True)

motor_torque_curve = gcurve(graph=torque_graph, color=color.blue)
net_torque_curve = gcurve(graph=torque_graph, color=color.orange)

# Physics parameters
# These values are subject to change
# The squirrel cage rotor has induced EMF/current because of slip, not because of a DC battery.
rotor_R = 0.8              # Rotor resistance
rotor_X_locked = 1.2       # Rotor reactance when slip is 1
k_induced = 0.80           # Converts slip speed into induced rotor EMF
k_t = 0.35                 # Converts rotor current into torque
J = 0.05                   # Moment of inertia
load_torque = 0.03         # Small opposing load
damping = 0.02             # Friction loss

# Initial conditions
theta = 0.2
omega = 0.0
dt = 0.002

def rotor_radius_change(evt):
    global rotor_radius
    rotor_radius = evt.value
    rotor_radius_text.text = 'Rotor Radius: '+str(rotor_radius)

def rotor_R_change(evt):
    global rotor_R
    rotor_R = evt.value
    rotor_R_text.text = 'Rotor Resistance: '+str(rotor_R)

scene.append_to_caption('\n\n')
rotor_radius_slider = slider(bind=rotor_radius_change, max=5, min=0.5, step=0.1)
rotor_radius_text = wtext(text='Rotor Radius: '+str(rotor_radius))
scene.append_to_caption('\n\n')
rotor_R_slider = slider(bind=rotor_R_change, max=5, min=0.5, step=0.1)
rotor_R_text = wtext(text='Rotor Resistance: '+str(rotor_R))
scene.append_to_caption('\n\n')

# Keeps an angle between -pi and pi
def wrap_angle(angle):
    return atan2(sin(angle), cos(angle))

# Calculates slip, induced EMF, current, motor torque, and net torque for an induction motor
def motor_values(omega):
    slip_speed = omega_sync - omega
    slip = slip_speed / omega_sync

    induced_emf = k_induced * slip_speed

    rotor_reactance = rotor_X_locked * abs(slip)
    rotor_impedance = sqrt(rotor_R**2 + rotor_reactance**2)

    current = induced_emf / rotor_impedance

    motor_torque = k_t * current**2 * rotor_R / omega_sync

    load_direction = 1 if omega >= 0 else -1
    net_torque = motor_torque - damping * omega - load_torque * load_direction

    return slip, induced_emf, current, motor_torque, net_torque

# Calculates the rotor's angular velocity and angular acceleration
def derivatives(theta, omega, t):
    slip, induced_emf, current, motor_torque, net_torque = motor_values(omega)

    alpha = net_torque / J

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

    new_theta = wrap_angle(new_theta)

    return new_theta, new_omega

# Updates the visual rotor bar and coil so they rotate together
def update_rotor_visuals(theta, t):
    # Three-phase stator currents create the rotating magnetic field
    ac1 = rmsI*sqrt(2)*sin(omega_electric*t)
    ac2 = rmsI*sqrt(2)*sin(omega_electric*t-2*pi/3)
    ac3 = rmsI*sqrt(2)*sin(omega_electric*t-4*pi/3)
       
    B1 = mu0*ac1*N/l*vector(cos(pi/2), sin(pi/2), 0)
    B2 = mu0*ac2*N/l*vector(cos(pi/2+2*pi/3), sin(pi/2+2*pi/3), 0)
    B3 = mu0*ac3*N/l*vector(cos(pi/2+4*pi/3), sin(pi/2+4*pi/3), 0)
    B = B1+B2+B3
   
    B1arrow.axis = B1 * B_visual_scale
    B2arrow.axis = B2 * B_visual_scale
    B3arrow.axis = B3 * B_visual_scale
    Barrow.axis = B * B_visual_scale
    
    end_ring_left.radius = rotor_radius
    end_ring_right.radius = rotor_radius
    
    # Rotate the squirrel cage rotor bars with the rotor
    for i in range(num_bars):
        angle = i * ((2 * pi) / num_bars) + pi/2 + theta
        bar_pos = vector(rotor_radius * cos(angle), rotor_radius * sin(angle), 0)
        rotor_bars[i].pos = bar_pos - vector(0, 0, rotor_length/2)
        rotor_bars[i].axis = vector(0, 0, rotor_length)

# Main animation loop
while True:
    rate(250)

    theta, omega = rk4_step(theta, omega, t, dt)

    field_angle = omega_sync * t

    stator_radius = 2

    update_rotor_visuals(theta, t)

    slip, induced_emf, current, motor_torque, net_torque = motor_values(omega)

    # This gives a sine-wave EMF while still making the amplitude depend on slip
    instant_emf = induced_emf * sin(wrap_angle(omega_sync * t - theta))

    emf_curve.plot(t, instant_emf)
    motor_torque_curve.plot(t, motor_torque)
    net_torque_curve.plot(t, net_torque)

    info.text = "Rotor speed: " + str(round(omega, 2)) + " rad/s\n" + \
                "Synchronous speed: " + str(round(omega_sync, 2)) + " rad/s\n" + \
                "Slip: " + str(round(slip * 100, 2)) + "%\n" + \
                "Instant EMF: " + str(round(instant_emf, 2)) + " V\n" + \
                "Rotor current: " + str(round(current, 2)) + " A\n" + \
                "Motor torque: " + str(round(motor_torque, 2)) + " Nm"
    t += dt
