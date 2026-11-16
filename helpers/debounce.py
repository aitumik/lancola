from machine import Pin
import time 

led = Pin(21,mode=Pin.OUT)

button = Pin(39,mode = Pin.IN,pull=Pin.PULL_UP)

led_state = False
last_time = 0
debounce = 500


while True:
    if button.value() == 1:
        current_time = time.ticks_ms()
        
        if time.ticks_diff(current_time,last_time) > debounce:
            led_state = not led_state
            led.value(led_state)
            last_time  = current_time
            
        while button.value() == 1:
            pass
        
    time.sleep_ms(20)
