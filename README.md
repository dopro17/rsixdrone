# DESCRIPTION

This is a "rainbow six like" robot, this prototype works with an esp32 MCU from espressif as control system. Its main features are: control over Wi-Fi network, HD FTV, sony ps4 joypad as main controller input at pc host. 

# Hardware

The actual prototype are a simple and very old remote control 2WD off road truck, because intended to be a test for CPU board and other hardware. In the future the hardware will be migrated to "rainbow six" like one.

The main features of this hardware are:

- 7.2v@1800mAh NiCd battery.
- DC motor for traction.
- DC motor and linear resistive encoder, for the steering system.

All this hardware is controlled by wroom32-cam dev-kit with micropython uOS system, ps4 joypad + pc host with python3 host side system.



# Lib rsix



### Class motor

------

```python
from rsix import motor

motor(pin_A, pin_B, freq=1000, name="objec name") #Initiate a hardware dc motor object
motor.speed(s) 		#set current ´speed` PWM dutty -1 >= s >= 1 (-100% to 100%).
motor.deinit() 		#deinit pwm pins, the objet can not be used after call this function.
    
```

#### Constructors 

- **`pin_A`** PWM H-bridge H-channel pin.

- **`pin_B`** PWM H-bridge L-channel pin.

- **`freq`** PWM period frequency in Hz.

- **`name`** Object name, helps to identify in *stdout* prints.

  

### Class linear_encoder

------

To be continued...

