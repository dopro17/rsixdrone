# DESCRIPTION

This is a "rainbow six like" robot, this prototype works with an esp32 MCU from espressif as control system. Its main features are: control over Wi-Fi network, HD FTV, sony ps4 joypad as main controller input at pc host. 

# Hardware

The actual prototype are a simple and very old remote control 2WD off road truck, because intended to be a test for CPU board and other hardware. In the future the hardware will be migrated to "rainbow six" like one.

The main features of this hardware are:

- 7.2v@1800mAh NiCd battery.
- DC motor for traction.
- DC motor and linear resistive encoder, for the steering system.

All this hardware is controlled by wroom32-cam dev-kit with micropython uOS system, L297N (dual H-Bridge) and a ps4 joypad + pc host with python3 host side system.



