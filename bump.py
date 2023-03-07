from pololu_3pi_plus_2040_robot import robot 
import time

buzzer = robot.Buzzer()
bump_sensors = robot.BumpSensors()
display= robot.Display()
motors= robot.Motors()
rgb_leds = robot.RGBLEDs()
rgb_leds.set_brightness(5)
button_a = robot.ButtonA()

display.fill(0)
display.text("Bump Demo", 0,0)
display.text("Press A to drive.",0, 20)
display.text("Hold bump sensor", 0, 40)
display.text("to stop.", 0, 50)
bump_sensors.calibrate()
display.show()

while not button_a.check():
    pass

def leds_yellow():
    rgb_leds.set(0, [255,100,0])
    rgb_leds.set(1, [255,100,0])
    rgb_leds.set(2, [255,100,0])
    rgb_leds.set(3, [0,0,0])
    rgb_leds.set(4, [0,0,0])
    rgb_leds.set(5, [0,0,0])
    rgb_leds.show()

def leds_green():
    rgb_leds.set(0, [0,0,0])
    rgb_leds.set(1, [0,0,0])
    rgb_leds.set(2, [0,0,0])
    rgb_leds.set(3, [0,255,0])
    rgb_leds.set(4, [0,255,0])
    rgb_leds.set(5, [0,255,0])
    rgb_leds.show()

def leds_red():
    rgb_leds.set(0, [255, 0,0])
    rgb_leds.set(1, [255, 0,0])
    rgb_leds.set(2, [255, 0,0])
    rgb_leds.set(3, [255, 0,0])
    rgb_leds.set(4, [255, 0,0])
    rgb_leds.set(5, [255, 0,0])
    rgb_leds.show()

# Blinks yellow LEDs for two seconds.
def blink_2s():
    leds_yellow()
    time.sleep_ms(500)
    rgb_leds.off()
    time.sleep_ms(500)
    leds_yellow()
    time.sleep_ms(500)
    rgb_leds.off()
    time.sleep_ms(500)
    
def back_up(message):
    display.fill(0)
    display.text(f"{message} sensor", 20,20)
    display.text("is pressed", 20,30)
    display.show()
    
    motors.off()
    leds_red()
    buzzer.play("t500 o3 ms bdad")
    time.sleep_ms(300)
    
    # Play four seconds of beeps.
    buzzer.play_in_background("t60 o6 ms c+c+c+c+")
    
    motors.set_speeds(-1500, -1500)
    display.fill(0)
    display.text("backing up!", 20,30)
    display.show()
    blink_2s()
    motors.set_speeds(0, -1500)
    blink_2s()

    motors.off()
    time.sleep_ms(500)

display.fill(0)
display.show()
try:
    while True:
        bump_sensors.read()
        leds_green()
        display.fill(0)
        display.text("moving forward!", 5,30)
        display.show()
        motors.set_speeds(4000,4000)
        
        if bump_sensors.left_is_pressed():
            b = "left"
        elif bump_sensors.right_is_pressed():
            b = "right"
        else:
            b = None
        
        if b:
            back_up(b)
            
            # If any of the bump sensors is held, end the program.
            bump_sensors.read()
            if bump_sensors.left_is_pressed() or bump_sensors.right_is_pressed():
                motors.off()
                break
                
finally:
    motors.off()
    rgb_leds.off()
    buzzer.off()
    
display.fill(0)
display.text("Goodbye", 20,30)
display.show()