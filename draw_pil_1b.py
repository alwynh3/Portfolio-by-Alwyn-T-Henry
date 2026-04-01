import tempfile
from PIL import Image, ImageDraw, ImageFont
import os

def create_block_diagram():
    width = 1100
    height = 800
    
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw faint blue notebook lines
    for y in range(50, height, 50):
        draw.line([(0, y), (width, y)], fill=(220, 230, 245), width=2)
        
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_med = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_small = ImageFont.load_default()

    box_color = (0, 0, 150)
    text_color = (0, 0, 150)
    line_color = (0, 0, 150)
    text_orange = (255, 140, 0)
    line_w = 4
    
    def draw_box(x, y, w, h, text=""):
        draw.rectangle([(x, y), (x+w, y+h)], outline=box_color, width=line_w)
        if text:
            draw.text((x + w/2 - 12, y + h/2 - 20), text, font=font_large, fill=text_color)
            
    def draw_arrow(x, y, direction="right"):
        if direction == "right":    draw.polygon([(x, y), (x-12, y-8), (x-12, y+8)], fill=box_color)
        elif direction == "left":   draw.polygon([(x, y), (x+12, y-8), (x+12, y+8)], fill=box_color)
        elif direction == "down":   draw.polygon([(x, y), (x-8, y-12), (x+8, y-12)], fill=box_color)
        elif direction == "up":     draw.polygon([(x, y), (x-8, y+12), (x+8, y+12)], fill=box_color)

    # ==========================
    # PART (b1): x is input, z is output
    # Equation: z(t) = x(t) + \int x(t) dt
    # ==========================
    
    draw.text((50, 60), "(b1) Treat x as input, z as output", font=font_large, fill=text_orange)
    draw.text((50, 100), "z(t) = x(t) + ∫ x(t) dt", font=font_med, fill=text_color)
    
    # Input x(t)
    start_x = 100
    start_y = 200
    draw.text((start_x + 20, start_y - 40), "x(t)", font=font_large, fill=text_color)
    draw.line([(start_x, start_y), (400, start_y)], fill=line_color, width=line_w)
    
    # Summing junction for z(t)
    sum1_x = 400
    sum1_y = 150
    draw_box(sum1_x, sum1_y, 40, 100)
    draw.text((sum1_x + 10, start_y - 15), "+", font=font_med, fill=text_color)
    draw.text((sum1_x + 10, start_y + 15), "+", font=font_med, fill=text_color)
    draw_arrow(sum1_x, start_y, "right")
    
    # Integrator branch
    # Dot at split point
    split1_x = 200
    draw.ellipse([(split1_x - 5, start_y - 5), (split1_x + 5, start_y + 5)], fill=box_color)
    
    # Branch going down and right to integrator
    int1_y = 280
    draw.line([(split1_x, start_y), (split1_x, int1_y), (250, int1_y)], fill=line_color, width=line_w)
    draw_arrow(250, int1_y, "right")
    
    int1_x = 250
    draw_box(int1_x, int1_y - 40, 60, 80, "∫")
    
    # Output of integrator going up to summing junction
    draw.line([(int1_x + 60, int1_y), (350, int1_y), (350, start_y + 30), (sum1_x, start_y + 30)], fill=line_color, width=line_w)
    draw_arrow(sum1_x, start_y + 30, "right")
    
    # Output z(t)
    draw.line([(sum1_x + 40, start_y), (550, start_y)], fill=line_color, width=line_w)
    draw_arrow(550, start_y, "right")
    draw.text((500, start_y - 40), "z(t)", font=font_large, fill=text_color)


    # ==========================
    # PART (b2): z is input, x is output
    # Equation: x(t) = z(t) - ∫ x(t) dt
    # ==========================
    
    draw.text((50, 410), "(b2) Treat z as input, x as output", font=font_large, fill=text_orange)
    draw.text((50, 450), "x(t) = z(t) - ∫ x(t) dt", font=font_med, fill=text_color)

    # Input z(t)
    start2_x = 100
    start2_y = 550
    draw.text((start2_x + 20, start2_y - 40), "z(t)", font=font_large, fill=text_color)
    draw.line([(start2_x, start2_y), (300, start2_y)], fill=line_color, width=line_w)
    
    # Summing junction for x(t)
    sum2_x = 300
    sum2_y = 500
    draw_box(sum2_x, sum2_y, 40, 100)
    draw.text((sum2_x + 10, start2_y - 15), "+", font=font_med, fill=text_color)
    draw.text((sum2_x + 10, start2_y + 15), "-", font=font_med, fill=text_color)
    draw_arrow(sum2_x, start2_y, "right")
    
    # the output is x(t) going right
    out2_x = 600
    draw.line([(sum2_x + 40, start2_y), (out2_x, start2_y)], fill=line_color, width=line_w)
    draw_arrow(out2_x, start2_y, "right")
    draw.text((550, start2_y - 40), "x(t)", font=font_large, fill=text_color)
    
    # Feedback branch for Integrator
    # Dot at split point
    split2_x = 450
    draw.ellipse([(split2_x - 5, start2_y - 5), (split2_x + 5, start2_y + 5)], fill=box_color)
    
    # Branch going down and left to integrator
    int2_y = 650
    draw.line([(split2_x, start2_y), (split2_x, int2_y), (400, int2_y)], fill=line_color, width=line_w)
    draw_arrow(400, int2_y, "left")
    
    int2_x = 340
    draw_box(int2_x, int2_y - 40, 60, 80, "∫")
    
    # Output of integrator going left and up to summing junction
    draw.line([(int2_x, int2_y), (250, int2_y), (250, start2_y + 30), (sum2_x, start2_y + 30)], fill=line_color, width=line_w)
    draw_arrow(sum2_x, start2_y + 30, "right")

    img.save("/Users/ty/Portfolio/diagram_1b.png")
    print("Done")

if __name__ == "__main__":
    create_block_diagram()
