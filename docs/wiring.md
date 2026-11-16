# Wiring and pins

## ESP32 pin rules

| Pins | Use |
|---|---|
| 4, 5, 13, 14, 16-19, 21-23, 25-27, 32, 33 | General input/output, PWM |
| 34, 35, 36 (VP), 39 (VN) | **Input only**, no internal pull-up/pull-down |
| 32-39 | Analog input on ADC1, works with Wi-Fi on |
| 0, 2, 4, 12-15, 25-27 | ADC2: analog stops working when Wi-Fi is on |
| 0, 2, 5, 12, 15 | Boot-mode pins: avoid things that pull them high/low at power-up |
| 6-11 | Used by the flash chip: never use |
| 21 (SDA), 22 (SCL) | I2C (LCD) |

Logic is 3.3V. Modules that output 5V (HC-SR04 ECHO) need a voltage divider.

## Default pins used in lancola

Every example runs on its own, so pins repeat between examples.
To use several parts at once, pick free pins and pass them in.

| Part | Pins (default) |
|---|---|
| LED | 23 |
| Button module | 39 |
| RGB LED | R 25, G 26, B 27 |
| Active / passive buzzer | 27 |
| Potentiometer | 36 |
| Photoresistor | 35 |
| PIR | 14 |
| DHT11 | 4 |
| Transistor base | 25 (through 1k) |
| LCD 1602 | SDA 21, SCL 22 |
| 7-segment | a 13, b 14, c 27, d 26, e 25, f 33, g 32, dp 23 |
| 4-digit tube | segments as above + D1 4, D2 16, D3 17, D4 18 |
| IR receiver | 19 |
| HC-SR04 | TRIG 18, ECHO 34 |
| Servo | 13 |
| Motor driver | IN1 25, IN2 26 |
| Keypad 4x4 | rows 19, 18, 5, 17; columns 16, 4, 33, 32 |

## Hardware timers

The ESP32 has timers 0-3. `ir_nec` uses timer 0 and `sevenseg.start()` uses
timer 1 by default. Pass `timer=` to change them if they clash.
