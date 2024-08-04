# ForCEs-Exoskeleton-Project
Project at Deggendorf Institute of Technology for the development of a lower-limb active exoskeleton.
Scientific publication about the exoskeleton can be found [here](https://doi.org/10.1109/CoDIT58514.2023.10284272).
The supporting Master Thesis work for the actuator development is available [here](docs/Masterarbeit_TCC_Aubeeluck.pdf).

## Description
The goal of this project was to design and develop an exoskeleton that can be worn with higher levels of acceptance
from patients. In particular, the actuator has a unique four-bar-linkage design, with a conventional belt-and-pulley drive
that allows it match the polycentric rotation of the knee and be back-driveable. 
The Control System of the exoskeleton relies on the operation of multiple interfaces, mainly a core running on a central processor, 
in this case, a portable Raspberry Pi 4 model B (4 Gb). Arduino Microcontrollers were used for Data Acquisition and ADC.
No specific HMI exists for the use and operation of the exoskeleton. Since an ODrive v3.4 controller is used for the motor control,
most testing and interactions have been achieved through CLI and basic python scripts.
The support structure is created with topology optimization and a prototype was assembled with powder printed parts.

## Structure


## Goal of this Repository
To complement the publication titled ["Design and Development of a knee rehabilitation exoskeleton with four-bar linkage actuation"](https://doi.org/10.1109/CoDIT58514.2023.10284272), so that the experimental trials, as well as results are made available and can be reproduced independently. This work has been completed by several researchers at the DIT and crediting us for any use of the material here would be very much appreciated.
For the image/build file for the Raspberry Pi and additional work with AI Gait recognition, please contact us.
