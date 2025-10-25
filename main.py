from machine import Pin, I2C
import ssd1306
import framebuf
import time
import math

i2c = I2C(0, scl=Pin(1), sda=Pin(0))  
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
def findit(oled):
    target = oled.height
    scale = target // 8            
    if scale < 1:
        scale = 1
    return scale
def render(word):
    w = len(word) * 8         
    h = 8
    buf = bytearray((w * h) // 8)  
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    fb.fill(0)
    fb.text(word, 0, 0)       
    return fb, w, h
def blit_scaled(oled, fb, fb_w, fb_h, x, y, scale):
    for px in range(fb_w):
        for py in range(fb_h):
            if fb.pixel(px, py): 
                oled.fill_rect(x + px * scale,
                               y + py * scale,
                               scale, scale, 1)

words = "Hello!"  
pause = 0.5
scroll_step = 12 
delay = 0.02 
while True:
    fb, fb_w, fb_h = render(words)
    scale = findit(oled)
    text_width = fb_w * scale
    start_x = oled.width
    y = (oled.height - fb_h * scale) // 2 
    for x in range(start_x, -text_width - 1, -scroll_step):
        oled.fill(0)
        blit_scaled(oled, fb, fb_w, fb_h, x, y, scale)
        oled.show()
        time.sleep(delay)
    time.sleep(pause)
