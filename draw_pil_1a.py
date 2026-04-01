import tempfile
from PIL import Image, ImageDraw, ImageFont
import os

def create_block_diagram():
    width = 1350  # Increased width to fit equations on the right
    height = 800
    
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw ruled lines
    for y in range(50, height, 50):
        draw.line([(0, y), (width, y)], fill=(220, 230, 245), width=2)
        
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()

    box_color = (0, 0, 150)
    text_color = (0, 0, 150)
    line_color = (0, 0, 150)
    line_w = 4
    
    def draw_box(x, y, w, h, text=""):
        draw.rectangle([(x, y), (x+w, y+h)], outline=box_color, width=line_w)
        if text:
            draw.text((x + w/2 - 12, y + h/2 - 20), text, font=font_large, fill=text_color)
            
    def draw_gain(x, y, w, h, text="", point_left=True):
        if point_left:
            points = [(x+w, y), (x, y+h/2), (x+w, y+h)]
        else:
            points = [(x, y), (x+w, y+h/2), (x, y+h)]
        draw.polygon(points, outline=box_color, width=line_w)
        if text:
            draw.text((x + w/2 - 5 if point_left else x + w/2 - 15, y + h/2 - 15), text, font=font_med, fill=text_color)

    def draw_arrow(x, y, direction="right"):
        if direction == "right":
            draw.polygon([(x, y), (x-12, y-8), (x-12, y+8)], fill=box_color)
        elif direction == "left":
            draw.polygon([(x, y), (x+12, y-8), (x+12, y+8)], fill=box_color)
        elif direction == "down":
            draw.polygon([(x, y), (x-8, y-12), (x+8, y-12)], fill=box_color)
        elif direction == "up":
            draw.polygon([(x, y), (x-8, y+12), (x+8, y+12)], fill=box_color)

    # --- TOP SYSTEM (X) ---
    sum_x_x = 250
    sum_x_y = 100
    sum_x_w = 40
    sum_x_h = 240
    draw_box(sum_x_x, sum_x_y, sum_x_w, sum_x_h)
    draw.text((sum_x_x+10, 130-15), "+", font=font_med, fill=text_color)
    draw.text((sum_x_x+10, 190-15), "-", font=font_med, fill=text_color)
    draw.text((sum_x_x+10, 250-15), "+", font=font_med, fill=text_color)
    draw.text((sum_x_x+10, 310-15), "-", font=font_med, fill=text_color)
    
    # f(t) input -> pin 130
    draw.line([(100, 130), (sum_x_x, 130)], fill=line_color, width=line_w)
    draw_arrow(sum_x_x, 130, "right")
    draw.text((120, 90), "f(t)", font=font_large, fill=text_color)
    
    # x'' line
    draw.line([(sum_x_x+sum_x_w, 220), (450, 220)], fill=line_color, width=line_w)
    draw_arrow(450, 220, "right")
    draw.text((340, 180), "x''(t)", font=font_large, fill=text_color)
    
    # Int 1
    int1_x = 450
    int1_y = 180
    draw_box(int1_x, int1_y, 60, 80, "∫")
    
    # x' line
    draw.line([(int1_x+60, 220), (610, 220)], fill=line_color, width=line_w)
    draw_arrow(610, 220, "right")
    draw.text((520, 180), "x'(t)", font=font_large, fill=text_color)
    draw.ellipse([(575, 215), (585, 225)], fill=box_color) # dot
    
    # Int 2
    int2_x = 610
    int2_y = 180
    draw_box(int2_x, int2_y, 60, 80, "∫")
    
    # x line
    draw.line([(int2_x+60, 220), (850, 220)], fill=line_color, width=line_w)
    draw_arrow(850, 220, "right")
    draw.text((720, 180), "x(t)", font=font_large, fill=text_color)
    draw.ellipse([(775, 215), (785, 225)], fill=box_color) # dot
    
    # --- BOTTOM SYSTEM (Y) ---
    sum_y_x = 250
    sum_y_y = 500
    sum_y_w = 40
    sum_y_h = 180
    draw_box(sum_y_x, sum_y_y, sum_y_w, sum_y_h)
    draw.text((sum_y_x+10, 530-15), "+", font=font_med, fill=text_color)
    draw.text((sum_y_x+10, 590-15), "+", font=font_med, fill=text_color)
    draw.text((sum_y_x+10, 650-15), "-", font=font_med, fill=text_color)
    
    # g(t) input -> gain 5 -> pin 530
    draw.line([(50, 530), (130, 530)], fill=line_color, width=line_w)
    draw_arrow(130, 530, "right")
    draw.text((60, 490), "g(t)", font=font_large, fill=text_color)
    draw_gain(130, 510, 50, 40, "5", point_left=False)
    draw.line([(180, 530), (sum_y_x, 530)], fill=line_color, width=line_w)
    draw_arrow(sum_y_x, 530, "right")
    
    # y' line
    draw.line([(sum_y_x+sum_y_w, 590), (510, 590)], fill=line_color, width=line_w)
    draw_arrow(510, 590, "right")
    draw.text((380, 550), "y'(t)", font=font_large, fill=text_color)
    draw.ellipse([(435, 585), (445, 595)], fill=box_color) # dot
    
    # Int 3
    int3_x = 510
    int3_y = 550
    draw_box(int3_x, int3_y, 60, 80, "∫")
    
    # y line
    draw.line([(int3_x+60, 590), (850, 590)], fill=line_color, width=line_w)
    draw_arrow(850, 590, "right")
    draw.text((720, 550), "y(t)", font=font_large, fill=text_color)
    draw.ellipse([(675, 585), (685, 595)], fill=box_color) # dot
    
    # --- FEEDBACK LOOPS ---
    
    # 2x' to SumX (pin 190) (-)
    draw.line([(580, 220), (580, 300), (500, 300)], fill=line_color, width=line_w)
    draw_arrow(500, 300, "left")
    draw_gain(450, 280, 50, 40, "2", point_left=True)
    draw.line([(450, 300), (210, 300), (210, 190), (sum_x_x, 190)], fill=line_color, width=line_w)
    draw_arrow(sum_x_x, 190, "right")

    # x to SumX (pin 310) (-) and SumY (pin 590) (+)
    draw.line([(780, 220), (780, 400), (150, 400)], fill=line_color, width=line_w)
    draw.line([(150, 400), (150, 310), (sum_x_x, 310)], fill=line_color, width=line_w)
    draw_arrow(sum_x_x, 310, "right")
    draw.line([(150, 400), (150, 590), (sum_y_x, 590)], fill=line_color, width=line_w)
    draw_arrow(sum_y_x, 590, "right")
    draw.ellipse([(145, 395), (155, 405)], fill=box_color) 

    # 2y' to SumX (pin 250) (+)
    draw.line([(440, 590), (440, 450), (400, 450)], fill=line_color, width=line_w)
    draw_arrow(400, 450, "left")
    draw_gain(350, 430, 50, 40, "2", point_left=True)
    draw.line([(350, 450), (230, 450), (230, 250), (sum_x_x, 250)], fill=line_color, width=line_w)
    draw_arrow(sum_x_x, 250, "right")

    # y to SumY (pin 650) (-)
    draw.line([(680, 590), (680, 700), (220, 700), (220, 650), (sum_y_x, 650)], fill=line_color, width=line_w)
    draw_arrow(sum_y_x, 650, "right")
    
    # EQUATIONS
    text_orange = (255, 140, 0)
    draw.text((900, 300), "or", font=font_large, fill=text_orange)
    draw.text((950, 300), "x''(t) = f(t) - 2x'(t) + 2y'(t) - x(t)", font=font_large, fill=text_orange)
    draw.text((950, 360), "y'(t) = 5g(t) + x(t) - y(t)", font=font_large, fill=text_orange)
    
    img.save("/Users/ty/Portfolio/diagram_1a.png")
    print("Done")

if __name__ == "__main__":
    create_block_diagram()
