# Ring for stator
# Helix for coil
# Box for battery / power source

from vpython import *
from math import sin, cos, pi, atan2, sqrt

# Setup
scene = canvas(title="AC Induction Motor Simulation",
               width=900,
               height=560,
               background=vector(0.96, 0.98, 1.0))

scene.forward = vector(0, 0, -1)
scene.center = vector(0, 0, 0)
scene.range = 4.1
scene.autoscale = False
scene.userzoom = False
scene.userspin = True
scene.userpan = True

# Default camera
base_center = vector(0, 0, 0)
base_forward = vector(0, 0, -1)
base_range = 4.1

# Default physics values
running = True
voltage_rms_default = 10.0
frequency_default = 0.80
rotor_R_default = 0.80
load_torque_default = 0.040
damping_default = 0.0030
J_default = 0.080
rotor_radius_default = 0.90
animation_steps_default = 3

# Motor settings
voltage_rms = voltage_rms_default
frequency = frequency_default
rotor_R = rotor_R_default
load_torque = load_torque_default
damping = damping_default
J = J_default
rotor_radius = rotor_radius_default
animation_steps = animation_steps_default

# Motor constants
phase_impedance = 3.0
poles = 2
N = 20
coil_length = 0.2
mu0 = 4*pi*1e-7
rotor_X_locked = 1.2
k_induced = 0.60
k_torque = 0.020
B_visual_scale = 900

# Time state
t = 0.0
theta = 0.2
omega = 0.0
dt = 0.003
plot_counter = 0
graph_window = 12.0

# Graph curve placeholders
ia_curve = None
ib_curve = None
ic_curve = None
speed_curve = None
sync_curve = None
emf_curve = None
motor_torque_curve = None
resist_torque_curve = None
net_torque_curve = None

# Display flags
live_visible = False
constants_visible = False

# Helper functions
def wrap_angle(angle):
    # Keeps an angle between -pi and pi.
    return atan2(sin(angle), cos(angle))


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def update_speeds():
    # Mechanical synchronous speed for a p-pole AC induction motor.
    omega_electric = 2*pi*frequency
    omega_sync = 4*pi*frequency/poles
    return omega_electric, omega_sync


def reset_view():
    # Camera reset only.
    scene.autoscale = False
    scene.center = base_center
    scene.forward = base_forward
    scene.range = base_range


def zoom_in():
    scene.autoscale = False
    scene.range = max(2.1, scene.range*0.85)


def zoom_out():
    scene.autoscale = False
    scene.range = min(7.5, scene.range*1.18)


def toggle_run():
    global running
    running = not running
    run_button.text = "Pause" if running else "Run"


def toggle_live_values():
    global live_visible
    live_visible = not live_visible
    live_button.text = "Hide Live Values" if live_visible else "Show Live Values"
    if not live_visible:
        live_text.text = ""


def toggle_constants():
    global constants_visible
    constants_visible = not constants_visible
    constants_button.text = "Hide Constants" if constants_visible else "Show Constants"
    if constants_visible:
        constants_text.text = constants_string()
    else:
        constants_text.text = ""


def constants_string():
    omega_electric, omega_sync = update_speeds()
    return "\nConstants\n" + \
           "Poles: " + str(poles) + "\n" + \
           "Turns per stator coil: " + str(N) + "\n" + \
           "Coil length: " + str(coil_length) + " m\n" + \
           "Phase impedance: " + str(phase_impedance) + " ohm\n" + \
           "Locked-rotor reactance: " + str(rotor_X_locked) + " ohm\n" + \
           "Time step: " + str(dt) + " s\n" + \
           "Synchronous speed now: " + str(round(omega_sync, 2)) + " rad/s\n"


# Stator ring
stator = shapes.circle(radius=2, thickness=0.1)

# Make it 3D
extrusion(path=[vec(0, 0, 0), vec(0, 0, 0.12)],
          shape=stator,
          color=color.gray(0.55))

# Stator coils for three-phase AC
coil_pairs = []
phase_colors = [color.red, color.green, color.blue]
phase_names = ["A", "B", "C"]

for i in range(3):
    thetaN = 5*pi/12 + i*pi/3
    thetaS = thetaN + pi
    offset = pi*0.08
    c = phase_colors[i]

    magnetN = shapes.arc(radius=1.8, thickness=0.50, angle1=thetaN, angle2=thetaN + pi/6)
    magnetS = shapes.arc(radius=1.8, thickness=0.50, angle1=thetaS, angle2=thetaS + pi/6)
    extrusion(path=[vec(0, 0, 0), vec(0, 0, 0.12)], shape=magnetN, color=color.gray(0.72))
    extrusion(path=[vec(0, 0, 0), vec(0, 0, 0.12)], shape=magnetS, color=color.gray(0.72))

    coilN = helix(pos=1.3*vector(cos(thetaN + offset), sin(thetaN + offset), 0),
                  axis=vector(cos(thetaN + pi/12), sin(thetaN + pi/12), 0),
                  radius=0.55,
                  thickness=0.035,
                  coils=N,
                  length=coil_length,
                  color=c)
    coilS = helix(pos=1.3*vector(cos(thetaS + offset), sin(thetaS + offset), 0),
                  axis=vector(cos(thetaS + pi/12), sin(thetaS + pi/12), 0),
                  radius=0.55,
                  thickness=0.035,
                  coils=N,
                  length=coil_length,
                  color=c)
    coil_pairs.append([coilN, coilS])

    label(pos=2.28*vector(cos(thetaN + pi/12), sin(thetaN + pi/12), 0),
          text="Phase " + phase_names[i],
          height=9,
          box=False,
          color=c)

# Magnetic field arrows
B1arrow = arrow(pos=vector(0, 0, 0.18), axis=vector(0, 0.2, 0), radius=0.035, color=color.red)
B2arrow = arrow(pos=vector(0, 0, 0.22), axis=vector(0, 0.2, 0), radius=0.035, color=color.green)
B3arrow = arrow(pos=vector(0, 0, 0.26), axis=vector(0, 0.2, 0), radius=0.035, color=color.blue)
Barrow = arrow(pos=vector(0, 0, 0.32), axis=vector(0, 1.0, 0), radius=0.065, color=color.black)
field_dot = sphere(pos=vector(0, 1.4, 0.35), radius=0.07, color=color.black)

# Axle through the motor
axle = cylinder(pos=vector(0, 0, -0.85),
                axis=vector(0, 0, 1.7),
                radius=0.06,
                color=color.black)

# Power source / battery box
battery = box(pos=vector(-3.05, 1.75, 0),
              size=vector(0.95, 0.50, 0.40),
              color=color.purple)

# Battery label
battery_label = label(pos=vector(-3.05, 2.18, 0),
                      text="3-phase AC",
                      height=11,
                      box=False,
                      color=color.black)

# AC source marks
plus_label = label(pos=vector(-2.68, 1.75, 0),
                   text="~",
                   height=18,
                   box=False,
                   color=color.black)

minus_label = label(pos=vector(-3.42, 1.75, 0),
                    text="~",
                    height=18,
                    box=False,
                    color=color.black)

# Wires from AC source to motor
wire1 = curve(pos=[vector(-2.65, 1.75, 0), vector(-1.70, 1.15, 0), vector(-1.18, 0.72, 0)],
              radius=0.025,
              color=color.red)
wire2 = curve(pos=[vector(-3.05, 1.50, 0), vector(-1.90, 0.0, 0), vector(-1.18, 0.0, 0)],
              radius=0.025,
              color=color.green)
wire3 = curve(pos=[vector(-3.45, 1.75, 0), vector(-1.90, -1.15, 0), vector(-1.18, -0.72, 0)],
              radius=0.025,
              color=color.blue)

# Squirrel Cage Rotor
rotor_length = 1.4
num_bars = 10
rotor_bars = []
bar_current_arrows = []

# 1. Create Rotor Bars
for i in range(num_bars):
    angle = i*((2*pi)/num_bars) + pi/2
    bar_pos = vector(rotor_radius*cos(angle), rotor_radius*sin(angle), 0)
    bar = cylinder(pos=bar_pos - vector(0, 0, rotor_length/2),
                   axis=vector(0, 0, rotor_length),
                   radius=0.035,
                   color=color.orange)
    rotor_bars.append(bar)

    current_arrow = arrow(pos=bar_pos - vector(0, 0, 0.18),
                          axis=vector(0, 0, 0.25),
                          radius=0.022,
                          color=color.cyan)
    bar_current_arrows.append(current_arrow)

# 2. Create End Rings
end_ring_left = ring(pos=vector(0, 0, -rotor_length/2),
                     axis=vector(0, 0, 1),
                     radius=rotor_radius,
                     thickness=0.06,
                     color=color.orange)
end_ring_right = ring(pos=vector(0, 0, rotor_length/2),
                      axis=vector(0, 0, 1),
                      radius=rotor_radius,
                      thickness=0.06,
                      color=color.orange)
rotor_marker = sphere(pos=vector(rotor_radius, 0, 0.76), radius=0.08, color=color.white)

# Physics functions
def stator_field_values(local_time):
    # Three-phase AC currents are 120 degrees apart.
    omega_electric, omega_sync = update_speeds()
    rmsI = voltage_rms/phase_impedance

    ia = rmsI*sqrt(2)*sin(omega_electric*local_time)
    ib = rmsI*sqrt(2)*sin(omega_electric*local_time - 2*pi/3)
    ic = rmsI*sqrt(2)*sin(omega_electric*local_time - 4*pi/3)

    B1 = mu0*ia*N/coil_length*vector(cos(pi/2), sin(pi/2), 0)
    B2 = mu0*ib*N/coil_length*vector(cos(pi/2 + 2*pi/3), sin(pi/2 + 2*pi/3), 0)
    B3 = mu0*ic*N/coil_length*vector(cos(pi/2 + 4*pi/3), sin(pi/2 + 4*pi/3), 0)
    B = B1 + B2 + B3

    return ia, ib, ic, B1, B2, B3, B


def motor_values(local_omega):
    # Slip is the fractional speed difference between the rotating field and rotor.
    omega_electric, omega_sync = update_speeds()
    slip = (omega_sync - local_omega)/omega_sync
    slip_for_calc = max(-2.0, min(2.0, slip))
    slip_abs = abs(slip_for_calc)
    torque_direction = sign(slip_for_calc)

    # In an induction motor, rotor EMF and rotor current frequency are proportional to slip.
    standstill_rotor_emf = k_induced*voltage_rms
    rotor_emf_rms = standstill_rotor_emf*slip_abs
    rotor_emf_peak = rotor_emf_rms*sqrt(2)
    rotor_reactance = rotor_X_locked*slip_abs
    rotor_impedance = sqrt(rotor_R**2 + rotor_reactance**2)
    rotor_current = rotor_emf_rms/rotor_impedance if rotor_impedance > 0 else 0

    # Simplified induction motor torque relation.
    # It rises from zero, then falls toward zero as slip approaches zero.
    torque_denominator = rotor_R**2 + (rotor_X_locked*slip_abs)**2
    if torque_denominator == 0 or slip_abs < 0.00001:
        motor_torque = 0
    else:
        motor_torque = torque_direction*k_torque*(standstill_rotor_emf**2)*rotor_R*slip_abs/(omega_sync*torque_denominator)

    friction = damping*local_omega
    if abs(local_omega) < 0.015 and abs(motor_torque) <= load_torque:
        load = motor_torque
    else:
        load = load_torque*(1 if local_omega >= 0 else -1)

    resisting_torque = load + friction
    net_torque = motor_torque - resisting_torque
    return slip, rotor_emf_rms, rotor_emf_peak, rotor_current, motor_torque, resisting_torque, net_torque


def derivatives(local_theta, local_omega, local_time):
    slip, rotor_emf_rms, rotor_emf_peak, rotor_current, motor_torque, resisting_torque, net_torque = motor_values(local_omega)
    alpha = net_torque/J
    return local_omega, alpha


def rk4_step(local_theta, local_omega, local_time, local_dt):
    # Fourth-order Runge-Kutta step for smoother rotor motion.
    k1_theta, k1_omega = derivatives(local_theta, local_omega, local_time)
    k2_theta, k2_omega = derivatives(local_theta + 0.5*local_dt*k1_theta,
                                     local_omega + 0.5*local_dt*k1_omega,
                                     local_time + 0.5*local_dt)
    k3_theta, k3_omega = derivatives(local_theta + 0.5*local_dt*k2_theta,
                                     local_omega + 0.5*local_dt*k2_omega,
                                     local_time + 0.5*local_dt)
    k4_theta, k4_omega = derivatives(local_theta + local_dt*k3_theta,
                                     local_omega + local_dt*k3_omega,
                                     local_time + local_dt)

    new_theta = local_theta + (local_dt/6)*(k1_theta + 2*k2_theta + 2*k3_theta + k4_theta)
    new_omega = local_omega + (local_dt/6)*(k1_omega + 2*k2_omega + 2*k3_omega + k4_omega)
    return wrap_angle(new_theta), new_omega


# Visual update functions
def update_rotor_visuals():
    global rotor_radius
    ia, ib, ic, B1, B2, B3, B = stator_field_values(t)
    slip, rotor_emf_rms, rotor_emf_peak, rotor_current, motor_torque, resisting_torque, net_torque = motor_values(omega)

    B1arrow.axis = B1*B_visual_scale
    B2arrow.axis = B2*B_visual_scale
    B3arrow.axis = B3*B_visual_scale
    Barrow.axis = B*B_visual_scale

    if mag(B) > 0:
        Bhat = norm(B)
    else:
        Bhat = vector(1, 0, 0)
    field_dot.pos = 1.45*Bhat + vector(0, 0, 0.35)

    end_ring_left.radius = rotor_radius
    end_ring_right.radius = rotor_radius

    field_angle = atan2(B.y, B.x)
    current_scale = 0.48*min(rotor_current/5.0, 1.25)

    # Rotate the squirrel cage rotor bars with the rotor.
    for i in range(num_bars):
        angle = i*((2*pi)/num_bars) + pi/2 + theta
        bar_pos = vector(rotor_radius*cos(angle), rotor_radius*sin(angle), 0)
        rotor_bars[i].pos = bar_pos - vector(0, 0, rotor_length/2)
        rotor_bars[i].axis = vector(0, 0, rotor_length)

        induced_direction = sin(wrap_angle(field_angle - angle))
        bar_current_arrows[i].pos = bar_pos - vector(0, 0, 0.18)
        bar_current_arrows[i].axis = vector(0, 0, current_scale*induced_direction)
        bar_current_arrows[i].color = color.cyan if induced_direction >= 0 else color.magenta

    rotor_marker.pos = vector(rotor_radius*cos(theta), rotor_radius*sin(theta), 0.76)


def live_values_string():
    omega_electric, omega_sync = update_speeds()
    ia, ib, ic, B1, B2, B3, B = stator_field_values(t)
    slip, rotor_emf_rms, rotor_emf_peak, rotor_current, motor_torque, resisting_torque, net_torque = motor_values(omega)
    instant_emf = rotor_emf_peak*sin(wrap_angle(atan2(B.y, B.x) - theta))

    status = "Running" if running else "Paused"
    if abs(omega) < 0.02 and abs(motor_torque) <= load_torque:
        status = status + " / stalled by load"

    return "\nLive Values\n" + \
           "Status: " + status + "\n" + \
           "Rotor speed: " + str(round(omega, 2)) + " rad/s\n" + \
           "Synchronous speed: " + str(round(omega_sync, 2)) + " rad/s\n" + \
           "Slip: " + str(round(slip*100, 2)) + "%\n" + \
           "Rotor EMF: " + str(round(rotor_emf_rms, 2)) + " V RMS\n" + \
           "Instant EMF: " + str(round(instant_emf, 2)) + " V\n" + \
           "Rotor current: " + str(round(rotor_current, 2)) + " A RMS\n" + \
           "Motor torque: " + str(round(motor_torque, 3)) + " Nm\n" + \
           "Resisting torque: " + str(round(resisting_torque, 3)) + " Nm\n" + \
           "Net torque: " + str(round(net_torque, 3)) + " Nm\n"


# Graph functions
def hide_curve(curve_object):
    if curve_object is None:
        return
    try:
        curve_object.delete()
    except Exception:
        try:
            curve_object.visible = False
        except Exception:
            pass


def create_graph_curves():
    global ia_curve, ib_curve, ic_curve, speed_curve, sync_curve, emf_curve
    global motor_torque_curve, resist_torque_curve, net_torque_curve

    ia_curve = gcurve(graph=current_graph, color=color.red)
    ib_curve = gcurve(graph=current_graph, color=color.green)
    ic_curve = gcurve(graph=current_graph, color=color.blue)

    speed_curve = gcurve(graph=speed_graph, color=color.orange)
    sync_curve = gcurve(graph=speed_graph, color=color.black)

    emf_curve = gcurve(graph=emf_graph, color=color.red)

    motor_torque_curve = gcurve(graph=torque_graph, color=color.blue)
    resist_torque_curve = gcurve(graph=torque_graph, color=color.red)
    net_torque_curve = gcurve(graph=torque_graph, color=color.orange)


def reset_graphs():
    # Fresh traces make reset behave like a page reload without creating new graph panels.
    global ia_curve, ib_curve, ic_curve, speed_curve, sync_curve, emf_curve
    global motor_torque_curve, resist_torque_curve, net_torque_curve

    for curve_object in [ia_curve, ib_curve, ic_curve, speed_curve, sync_curve, emf_curve,
                         motor_torque_curve, resist_torque_curve, net_torque_curve]:
        hide_curve(curve_object)

    # Return graph windows to the beginning so reset does not plot off-screen.
    for graph_object in [current_graph, speed_graph, emf_graph, torque_graph]:
        try:
            graph_object.xmin = 0
            graph_object.xmax = graph_window
        except Exception:
            pass

    create_graph_curves()


def plot_graphs():
    ia, ib, ic, B1, B2, B3, B = stator_field_values(t)
    slip, rotor_emf_rms, rotor_emf_peak, rotor_current, motor_torque, resisting_torque, net_torque = motor_values(omega)
    omega_electric, omega_sync = update_speeds()
    instant_emf = rotor_emf_peak*sin(wrap_angle(atan2(B.y, B.x) - theta))

    # x time starts at zero again after reset.
    graph_time = t
    ia_curve.plot(graph_time, ia)
    ib_curve.plot(graph_time, ib)
    ic_curve.plot(graph_time, ic)
    speed_curve.plot(graph_time, omega)
    sync_curve.plot(graph_time, omega_sync)
    emf_curve.plot(graph_time, instant_emf)
    motor_torque_curve.plot(graph_time, motor_torque)
    resist_torque_curve.plot(graph_time, resisting_torque)
    net_torque_curve.plot(graph_time, net_torque)


# Slider callback functions
def voltage_change(evt):
    global voltage_rms
    voltage_rms = evt.value
    voltage_text.text = str(round(voltage_rms, 1)) + " V"


def frequency_change(evt):
    global frequency
    frequency = evt.value
    frequency_text.text = str(round(frequency, 2)) + " Hz"


def rotor_R_change(evt):
    global rotor_R
    rotor_R = evt.value
    rotor_R_text.text = str(round(rotor_R, 2)) + " ohm"


def load_torque_change(evt):
    global load_torque
    load_torque = evt.value
    load_text.text = str(round(load_torque, 3)) + " Nm"


def damping_change(evt):
    global damping
    damping = evt.value
    damping_text.text = str(round(damping, 4))


def inertia_change(evt):
    global J
    J = evt.value
    inertia_text.text = str(round(J, 3)) + " kg m^2"


def rotor_radius_change(evt):
    global rotor_radius
    rotor_radius = evt.value
    rotor_radius_text.text = str(round(rotor_radius, 2))


def animation_speed_change(evt):
    global animation_steps
    animation_steps = int(evt.value)
    animation_speed_text.text = str(animation_steps) + "x"


# Reset function
def reset_simulation():
    global running, voltage_rms, frequency, rotor_R, load_torque, damping, J, rotor_radius
    global animation_steps, t, theta, omega, plot_counter, live_visible, constants_visible

    running = True
    voltage_rms = voltage_rms_default
    frequency = frequency_default
    rotor_R = rotor_R_default
    load_torque = load_torque_default
    damping = damping_default
    J = J_default
    rotor_radius = rotor_radius_default
    animation_steps = animation_steps_default

    t = 0.0
    theta = 0.2
    omega = 0.0
    plot_counter = 0

    run_button.text = "Pause"
    voltage_slider.value = voltage_rms
    frequency_slider.value = frequency
    rotor_R_slider.value = rotor_R
    load_slider.value = load_torque
    damping_slider.value = damping
    inertia_slider.value = J
    rotor_radius_slider.value = rotor_radius
    animation_speed_slider.value = animation_steps

    voltage_text.text = str(round(voltage_rms, 1)) + " V"
    frequency_text.text = str(round(frequency, 2)) + " Hz"
    rotor_R_text.text = str(round(rotor_R, 2)) + " ohm"
    load_text.text = str(round(load_torque, 3)) + " Nm"
    damping_text.text = str(round(damping, 4))
    inertia_text.text = str(round(J, 3)) + " kg m^2"
    rotor_radius_text.text = str(round(rotor_radius, 2))
    animation_speed_text.text = str(animation_steps) + "x"

    live_visible = False
    constants_visible = False
    live_button.text = "Show Live Values"
    constants_button.text = "Show Constants"
    live_text.text = ""
    constants_text.text = ""

    reset_view()
    reset_graphs()
    update_rotor_visuals()
    plot_graphs()


# Controls and instructions
scene.append_to_caption("\nControls\n")
run_button = button(bind=toggle_run, text="Pause", color=color.black)
scene.append_to_caption("  ")
button(bind=reset_simulation, text="Reset", color=color.black)
scene.append_to_caption("  ")
button(bind=zoom_in, text="Zoom In", color=color.black)
scene.append_to_caption("  ")
button(bind=zoom_out, text="Zoom Out", color=color.black)
scene.append_to_caption("  ")
button(bind=reset_view, text="Reset View", color=color.black)

scene.append_to_caption("\n\nSliders\n")
scene.append_to_caption("Voltage RMS:       ")
voltage_slider = slider(bind=voltage_change, min=2, max=20, value=voltage_rms, step=0.5, length=300)
voltage_text = wtext(text=str(round(voltage_rms, 1)) + " V")

scene.append_to_caption("\nFrequency:         ")
frequency_slider = slider(bind=frequency_change, min=0.25, max=2.0, value=frequency, step=0.05, length=300)
frequency_text = wtext(text=str(round(frequency, 2)) + " Hz")

scene.append_to_caption("\nRotor resistance:  ")
rotor_R_slider = slider(bind=rotor_R_change, min=0.2, max=2.5, value=rotor_R, step=0.05, length=300)
rotor_R_text = wtext(text=str(round(rotor_R, 2)) + " ohm")

scene.append_to_caption("\nLoad torque:       ")
load_slider = slider(bind=load_torque_change, min=0.0, max=0.25, value=load_torque, step=0.005, length=300)
load_text = wtext(text=str(round(load_torque, 3)) + " Nm")

scene.append_to_caption("\nFriction:          ")
damping_slider = slider(bind=damping_change, min=0.0, max=0.025, value=damping, step=0.0005, length=300)
damping_text = wtext(text=str(round(damping, 4)))

scene.append_to_caption("\nRotor inertia:     ")
inertia_slider = slider(bind=inertia_change, min=0.02, max=0.25, value=J, step=0.01, length=300)
inertia_text = wtext(text=str(round(J, 3)) + " kg m^2")

scene.append_to_caption("\nRotor visual size: ")
rotor_radius_slider = slider(bind=rotor_radius_change, min=0.55, max=1.15, value=rotor_radius, step=0.05, length=300)
rotor_radius_text = wtext(text=str(round(rotor_radius, 2)))

scene.append_to_caption("\nAnimation speed:   ")
animation_speed_slider = slider(bind=animation_speed_change, min=1, max=8, value=animation_steps, step=1, length=300)
animation_speed_text = wtext(text=str(animation_steps) + "x")

scene.append_to_caption("\n\nManual\n")
scene.append_to_caption("Drag to rotate. Shift-drag to pan. Scroll to zoom. Reset View only resets the camera. Reset restarts the whole simulation.\n")
scene.append_to_caption("Black arrow = net rotating magnetic field. Red/green/blue arrows = phase fields. Orange cage = rotor. Cyan/magenta arrows = induced rotor currents.\n")
scene.append_to_caption("Raise load torque to make the motor slow down or stall. Raise frequency to increase synchronous speed.\n")

scene.append_to_caption("\n")
live_button = button(bind=toggle_live_values, text="Show Live Values", color=color.black)
scene.append_to_caption("  ")
constants_button = button(bind=toggle_constants, text="Show Constants", color=color.black)
scene.append_to_caption("\n")
live_text = wtext(text="")
constants_text = wtext(text="")

scene.append_to_caption("\nGraphs\n")

# Graphs are created after the controls so they stay below the simulation area.
current_graph = graph(title="Three-phase stator currents",
                      xtitle="Time (s)",
                      ytitle="Current (A)",
                      width=900,
                      height=210,
                      xmin=0,
                      xmax=graph_window,
                      scroll=True)

speed_graph = graph(title="Rotor speed and synchronous speed",
                    xtitle="Time (s)",
                    ytitle="Speed (rad/s)",
                    width=900,
                    height=210,
                    xmin=0,
                    xmax=graph_window,
                    scroll=True)

emf_graph = graph(title="Instantaneous rotor EMF",
                  xtitle="Time (s)",
                  ytitle="EMF (V)",
                  width=900,
                  height=210,
                  xmin=0,
                  xmax=graph_window,
                  scroll=True)

torque_graph = graph(title="Torque balance",
                     xtitle="Time (s)",
                     ytitle="Torque (Nm)",
                     width=900,
                     height=210,
                     xmin=0,
                     xmax=graph_window,
                     scroll=True)

create_graph_curves()
update_rotor_visuals()
plot_graphs()

# Main animation loop
while True:
    rate(120)
    scene.autoscale = False

    if running:
        for i in range(animation_steps):
            theta, omega = rk4_step(theta, omega, t, dt)
            t += dt

    update_rotor_visuals()

    if running:
        plot_counter += 1
        if plot_counter % 5 == 0:
            plot_graphs()

    if live_visible:
        live_text.text = live_values_string()

    if constants_visible:
        constants_text.text = constants_string()
