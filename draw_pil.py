import tempfile
from PIL import Image, ImageDraw, ImageFont
import os

def create_block_diagram():
    # Since schemdraw is proving tricky to align perfectly like the handwritten 
    # example without excessive trial and error, I'll draw it precisely with PIL
    # to match the layout of the image.
    
    # Image dimensions
    width = 1200
    height = 800
    
    # Create white background with faint blue lines like notebook paper
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw ruled lines
    for y in range(50, height, 50):
        draw.line([(0, y), (width, y)], fill=(220, 230, 245), width=2)
        
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()

    # Colors
    box_color = (0, 0, 150) # Dark blue like pen
    text_color = (0, 0, 150)
    line_color = (0, 0, 150)
    line_w = 4
    
    # Function to draw a box
    def draw_box(x, y, w, h, text=""):
        draw.rectangle([(x, y), (x+w, y+h)], outline=box_color, width=line_w)
        if text:
            # simple centering
            draw.text((x + w/2 - 10, y + h/2 - 15), text, font=font_large, fill=text_color)
            
    # Function to draw a triangle (gain)
    def draw_gain(x, y, w, h, text="", point_left=True):
        if point_left:
            points = [(x+w, y), (x, y+h/2), (x+w, y+h)]
        else:
            points = [(x, y), (x+w, y+h/2), (x, y+h)]
        draw.polygon(points, outline=box_color, width=line_w)
        if text:
            draw.text((x + w/2 - 5 if point_left else 10, y + h/2 - 15), text, font=font_med, fill=text_color)

    # --- TOP SYSTEM (x) ---
    
    # Summing Box X
    sum_x_x = 250
    sum_x_y = 100
    sum_x_w = 40
    sum_x_h = 160
    draw_box(sum_x_x, sum_x_y, sum_x_w, sum_x_h)
    draw.text((sum_x_x+10, sum_x_y+10), "+", font=font_med, fill=text_color)
    draw.text((sum_x_x+10, sum_x_y+65), "-", font=font_med, fill=text_color)
    draw.text((sum_x_x+10, sum_x_y+120), "+", font=font_med, fill=text_color)
    
    # f(t) input
    draw.line([(100, sum_x_y+20), (sum_x_x, sum_x_y+20)], fill=line_color, width=line_w)
    draw.polygon([(sum_x_x, sum_x_y+20), (sum_x_x-10, sum_x_y+15), (sum_x_x-10, sum_x_y+25)], fill=box_color)
    draw.text((120, sum_x_y-20), "f(t)", font=font_large, fill=text_color)
    
    # x_ddot to Int 1
    draw.line([(sum_x_x+sum_x_w, sum_x_y+40), (450, sum_x_y+40)], fill=line_color, width=line_w)
    draw.polygon([(450, sum_x_y+40), (440, sum_x_y+35), (440, sum_x_y+45)], fill=box_color)
    draw.text((330, sum_x_y), "x''(t)", font=font_large, fill=text_color)
    
    # Int 1
    int1_x = 450
    int1_y = sum_x_y
    draw_box(int1_x, int1_y, 60, 80, "∫")
    
    # x_dot to Int 2
    draw.line([(int1_x+60, sum_x_y+40), (600, sum_x_y+40)], fill=line_color, width=line_w)
    draw.polygon([(600, sum_x_y+40), (590, sum_x_y+35), (590, sum_x_y+45)], fill=box_color)
    draw.text((540, sum_x_y), "x'(t)", font=font_large, fill=text_color)
    draw.ellipse([(525, sum_x_y+35), (535, sum_x_y+45)], fill=box_color) # junction dot
    
    # Int 2
    int2_x = 600
    int2_y = sum_x_y
    draw_box(int2_x, int2_y, 60, 80, "∫")
    
    # x output
    draw.line([(int2_x+60, sum_x_y+40), (800, sum_x_y+40)], fill=line_color, width=line_w)
    draw.polygon([(800, sum_x_y+40), (790, sum_x_y+35), (790, sum_x_y+45)], fill=box_color)
    draw.text((720, sum_x_y), "x(t)", font=font_large, fill=text_color)
    draw.ellipse([(750, sum_x_y+35), (760, sum_x_y+45)], fill=box_color) # junction dot
    
    
    # --- BOTTOM SYSTEM (y) ---
    sum_y_x = 250
    sum_y_y = 500
    sum_y_w = 40
    sum_y_h = 200
    draw_box(sum_y_x, sum_y_y, sum_y_w, sum_y_h)
    draw.text((sum_y_x+10, sum_y_y+20), "+", font=font_med, fill=text_color)
    draw.text((sum_y_x+10, sum_y_y+70), "+", font=font_med, fill=text_color)
    draw.text((sum_y_x+10, sum_y_y+120), "+", font=font_med, fill=text_color)
    draw.text((sum_y_x+10, sum_y_y+170), "-", font=font_med, fill=text_color)
    
    # g(t) input
    draw.line([(100, sum_y_y+30), (sum_y_x, sum_y_y+30)], fill=line_color, width=line_w)
    draw.polygon([(sum_y_x, sum_y_y+30), (sum_y_x-10, sum_y_y+25), (sum_y_x-10, sum_y_y+35)], fill=box_color)
    draw.text((120, sum_y_y-10), "g(t)", font=font_large, fill=text_color)
    
    # y_dot to Int 3
    draw.line([(sum_y_x+sum_y_w, sum_y_y+100), (550, sum_y_y+100)], fill=line_color, width=line_w)
    draw.polygon([(550, sum_y_y+100), (540, sum_y_y+95), (540, sum_y_y+105)], fill=box_color)
    draw.text((450, sum_y_y+50), "y'(t)", font=font_large, fill=text_color)
    
    # Int 3
    int3_x = 550
    int3_y = sum_y_y+50
    draw_box(int3_x, int3_y, 60, 100, "∫")
    
    # y output
    draw.line([(int3_x+60, sum_y_y+100), (800, sum_y_y+100)], fill=line_color, width=line_w)
    draw.polygon([(800, sum_y_y+100), (790, sum_y_y+95), (790, sum_y_y+105)], fill=box_color)
    draw.text((700, sum_y_y+50), "y(t)", font=font_large, fill=text_color)
    draw.ellipse([(670, sum_y_y+95), (680, sum_y_y+105)], fill=box_color) # junction dot
    
    
    # --- FEEDBACK LOOPS ---
    
    # x_dot gain 5 loop
    gain5_x = 450
    gain5_y = 220
    draw_gain(gain5_x, gain5_y, 50, 40, "5", True)
    draw.line([(530, sum_x_y+40), (530, gain5_y+20), (gain5_x+50, gain5_y+20)], fill=line_color, width=line_w) # down into gain
    draw.polygon([(gain5_x+50, gain5_y+20), (gain5_x+60, gain5_y+15), (gain5_x+60, gain5_y+25)], fill=box_color)
    
    # x_dot to gain 5 to sum_y (+) [Second plus on sum_y]
    draw.line([(gain5_x, gain5_y+20), (180, gain5_y+20), (180, sum_y_y+80), (sum_y_x, sum_y_y+80)], fill=line_color, width=line_w)
    draw.polygon([(sum_y_x, sum_y_y+80), (sum_y_x-10, sum_y_y+75), (sum_y_x-10, sum_y_y+85)], fill=box_color)
    draw.ellipse([(175, gain5_y+15), (185, gain5_y+25)], fill=box_color) # junction dot
    # also goes to sum_x (-) [From x_dot, actually the handwritten diagram has a loop from x_dot but no gain to - pin]
    draw.line([(180, gain5_y+20), (180, sum_x_y+75), (sum_x_x, sum_x_y+75)], fill=line_color, width=line_w)
    draw.polygon([(sum_x_x, sum_x_y+75), (sum_x_x-10, sum_x_y+70), (sum_x_x-10, sum_x_y+80)], fill=box_color)


    # x gain 3 loop
    gain3_x = 650
    gain3_y = 300
    draw_gain(gain3_x, gain3_y, 70, 50, "3", True)
    draw.line([(755, sum_x_y+40), (755, gain3_y+25), (gain3_x+70, gain3_y+25)], fill=line_color, width=line_w)
    
    # x to gain 3 to sum_y (+) [Third plus on sum_y]
    draw.line([(gain3_x, gain3_y+25), (130, gain3_y+25), (130, sum_y_y+130), (sum_y_x, sum_y_y+130)], fill=line_color, width=line_w)
    draw.polygon([(sum_y_x, sum_y_y+130), (sum_y_x-10, sum_y_y+125), (sum_y_x-10, sum_y_y+135)], fill=box_color)
    draw.ellipse([(125, gain3_y+20), (135, gain3_y+30)], fill=box_color) # junction dot
    
    # also goes to sum_x (+) [Bottom pin]
    draw.line([(130, gain3_y+25), (130, sum_x_y+130), (sum_x_x, sum_x_y+130)], fill=line_color, width=line_w)
    draw.polygon([(sum_x_x, sum_x_y+130), (sum_x_x-10, sum_x_y+125), (sum_x_x-10, sum_x_y+135)], fill=box_color)

    # y gain 3 loop
    gain3y_x = 550
    gain3y_y = 400
    draw_gain(gain3y_x, gain3y_y, 50, 40, "3", True)
    draw.line([(675, sum_y_y+100), (675, gain3y_y+20), (gain3y_x+50, gain3y_y+20)], fill=line_color, width=line_w)
    
    # y to gain 3 to sum_x (+) [Bottom pin, actually no y goes to sum_y(-)]
    draw.line([(gain3y_x, gain3y_y+20), (80, gain3y_y+20), (80, sum_y_y+180), (sum_y_x, sum_y_y+180)], fill=line_color, width=line_w)
    draw.polygon([(sum_y_x, sum_y_y+180), (sum_y_x-10, sum_y_y+175), (sum_y_x-10, sum_y_y+185)], fill=box_color)
    
    
    # adding the equations block to the side
    text_orange = (255, 140, 0)
    draw.text((850, 200), "or", font=font_large, fill=text_orange)
    draw.text((950, 200), "x''(t) = f(t) - 3(x - y)", font=font_large, fill=text_orange)
    draw.text((950, 250), "y'(t) = g(t) + 5x' + 3(x - y)", font=font_large, fill=text_orange)
    
    img.save("/Users/ty/Portfolio/handwritten_diagram.png")
    print("Done")

if __name__ == "__main__":
    create_block_diagram()
