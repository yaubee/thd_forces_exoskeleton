# ForCEs-Exoskeleton-Project
Project at Deggendorf Institute of Technology for the development of a lower-limb active exoskeleton.
Scientific publication about the exoskeleton can be found [here](https://doi.org/10.1109/CoDIT58514.2023.10284272).
The supporting Master Thesis work for the actuator development is available [here](docs/Masterarbeit_TCC_Aubeeluck.pdf).

Images of the the exoskeleton CAD model and completed 3D-printed model.
![cad_exoskeleton](docs/images/complete_exoskeleton_cad.PNG)
Fig. 1: CAD model of complete exoskeleton

![actual_exoskeleton](docs/images/complete_exoskeleton_actual.PNG)
Fig. 1: Actual exoskeleton

## Description
The goal of this project was to design and develop an exoskeleton that can be worn with higher levels of acceptance
from patients. In particular, the actuator has a unique four-bar-linkage design, with a conventional belt-and-pulley drive
that allows it match the polycentric rotation of the knee and be back-driveable. 
The Control System of the exoskeleton relies on the operation of multiple interfaces, mainly a core running on a central processor, 
in this case, a portable Raspberry Pi 4 model B (4 Gb). Arduino Microcontrollers were used for Data Acquisition and ADC.
No specific HMI exists for the use and operation of the exoskeleton. Since an ODrive v3.6 controller is used for the motor control,
most testing and interactions have been achieved through CLI and basic python scripts.
The support structure is created with topology optimization and a prototype was assembled with powder printed parts.

## Structure


## Goal of this Repository
To complement the publication titled ["Design and Development of a knee rehabilitation exoskeleton with four-bar linkage actuation"](https://doi.org/10.1109/CoDIT58514.2023.10284272), so that the experimental trials, as well as results are made available and can be reproduced independently. This work has been completed by several researchers at the DIT and crediting us for any use of the material here would be very much appreciated.
For the image/build file for the Raspberry Pi and additional work with AI Gait recognition, please contact us.

## Electronic Components:

The circuit schematic for the exoskeleton control is illustrated in the figure below:

![circuit_schematic](docs/images/circuit_schematic.PNG)Fig. 3: Circuit Schematic for Exoskeleton


These are the components used:

| Part Number | Part Name                | Part Description                               |
|-------------|---------------------------|------------------------------------------------|
| 1           | Battery                   | 22.2 V, ~5000 mAh LiPo Battery                 |
| 2           | Fuse Holder               | Fuse rating > 8 A                             |
| 3           | On/Off Switch             | DPST or DPDT Switch rated at 10 A             |
| 4           | Emergency Switch          | DPST Emergency Switch at 10 A                 |
| 5           | DC-DC Step Down Converter | 22.2 V to 5 V, 4A XL4016 Converter             |
| 6           | Emergency Push Button     | Latching Push Button rated at 2 A             |
| 7           | Mechanical Relay          | Relay rated at 10 A                           |
| 8           | ODrive Motor Controller   | ODrive v3.6 Dual BLDC Motor Controller (24V, 6A) |
| 9           | Braking Resistor          | 50W 0.5Ω Braking Resistor                     |
| 10          | Motor Encoder             | AMT-102V CUI Incremental Encoder              |
| 11          | BLDC Motor                | T-Motor P60 340KV BLDC Motor                  |
| 12          | Microcontroller           | Arduino Mega 2560 Microcontroller (12V, 2A)  |
| 13          | Angle Sensor             | AS5048A Magnetic Angle Sensor                |
| 14          | Push Button               | Latching Push Button (2A)                     |
| 15          | RGB LED                   | Common Anode RGB LED                         |

## Mechanical Components:

The actuator exploded view and cross-section are illustrated in the images below.
Parts were 3D-printed with SLS (EOS Selective Laser Sintering) and HP MJF (Multi Jet Fusion), as well as machined via 
conventional means.


![exploded_view_actuator](docs/images/actuator_exploded_view.PNG)Fig. 4: Exploded view of actuator and details of components.

![cross_section_view_actuator](docs/images/actuator_cross_section.PNG)Fig. 5: Cross-section view of actuator and details of components.

The four-bar-linkage is incorporated inside the actuator for a seamless design.
![four_bar_linkage_parts](docs/images/four_bar_linkage_3d.PNG)Fig. 6: Parts of the four-bar linkage.

![four_bar_linkage_2d](docs/images/four_bar_linkage_2d.PNG)Fig. 7: Four-bar linkage dimensions.
![four_bar_linkage_dimensions](docs/images/four_bar_linkage_dimensions.PNG)Fig. 8: Links in the four-bar linkage.

The torque sensor was machined via CNC-milling in Aluminum 7075. The dimensions for the torque sensor machining is shown below. ![torque_sensor_dimensions](docs/images/torque_sensor_2d_sketch.PNG)Fig. 9: Torque sensor element dimensions

