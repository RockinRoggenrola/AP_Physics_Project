# 3-Phase AC Induction Motor

A 3-phase AC induction motor consists of two main components: the stator and rotor, both of which are circular.
The stator has 3-phase AC current as input, which consists of 3 AC signals, having phase differences of 120 degrees.
Each of these 3 AC signals correspond to the red, green, and blue coils/wires. For example, the red wire carries
an AC current connecting the two red coils, which results in a changing magnetic field between the two red wires.
Similarly, there are AC currents running through the blue and green wires connecting the blue/green coils (which
are out of phase with the red AC current), creating 2 other magnetic fields, which combine in the center of the
stator to make a magnetic field which happens to rotate, indicated by the black arrow. The magnetic fields of the
colored coils are shown in the center as well with arrows of the corresponding colors.

To change the voltage of the current, change the value fo the Voltage RMS slider. Since AC voltage oscillates, RMS
voltage represents the voltage of a DC current with the equivalent power to the AC current. To change the frequency
of the AC currents, change the value of the Frequency slider.

The (squirrel-cage) rotor is within the center of the stator, and is made of a conducting material, with holes
within the the material. Because of the rotating magnetic field, there is a change of magnetic flux throughout
these openings, so by Faraday's Law, there is an induced current within the rotor, creating its own magnetic field,
which exerts a force and thus a torque on the circuitry of the rotor, so the rotor rotates. Certain properties of
the rotor can be changed, such as the resistance, load torque (the torque required to overcome the disk-shaped load
attached to the back of the rotor), inertia of the rotor, a frictional coefficient that represents the damping
on the motor, that may be caused by factors such as air resistance, and the rotor size. Each of these 5 factors
can be changed with their respective sliders.

The camera angle of the simulation can be changed by pressing shift and moving the mouse around while pressing. The
Zoom In and Zoom Out buttons can be used to change the zoom in the simulation, and the Reset View button can be
used to reset the camera angle of the simulation. The Reset button is used to reset the entire simulation, and the
Pause button pauses the simulation in time.

The outputs of the program can be viewed/hidden by pressing the Show/Hide Live Values/Constants buttons. The live
values display the rotor speed, synchronous speed (speed of the stator magnetic field), the slip (the percentage of
how much the rotor speed lags behind the synchronous speed), the RMS rotor EMF/current, the motor torque, resisting
torque, and the net torque (which goes to 0 in the long run). The constants display the number of poles, turns per
coil, coil length, phase impedance, locked-rotor reactance, time-step, and synchronous speed.

Below these, there are four graphs displaying the change of values over time, including the 3 stator phase currents
over time, rotor speed (yellow) and synchronous speed (black) over time, the instant rotor EMF (which oscillates),
and the different torques involved, including the motor torque (blue), the resisting torque (red), and the net
torque (orange).
