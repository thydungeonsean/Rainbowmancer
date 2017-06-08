
RED_5 = (250, 10, 0)
RED_4 = (215, 10, 0)
RED_3 = (200, 10, 0)
RED_2 = (170, 10, 0)
RED_1 = (150, 10, 0)

red_shades = {
5: RED_5,
4: RED_4,
3: RED_3,
2: RED_2,
1: RED_1
}

GREEN_5 = (25, 250, 0)
GREEN_4 = (25, 215, 0)
GREEN_3 = (25, 200, 0)
GREEN_2 = (25, 170, 0)
GREEN_1 = (25, 150, 0)

green_shades = {
5: GREEN_5,
4: GREEN_4,
3: GREEN_3,
2: GREEN_2,
1: GREEN_1
}

BLUE_5 = (25, 0, 250)
BLUE_4 = (25, 0, 215)
BLUE_3 = (25, 0, 200)
BLUE_2 = (25, 0, 170)
BLUE_1 = (25, 0, 150)

blue_shades = {
5: BLUE_5,
4: BLUE_4,
3: BLUE_3,
2: BLUE_2,
1: BLUE_1
}

YELLOW_5 = (255, 240, 0)
YELLOW_4 = (235, 222, 0)
YELLOW_3 = (220, 210, 0)
YELLOW_2 = (200, 190, 0)
YELLOW_1 = (180, 170, 0)

yellow_shades = {
5: YELLOW_5,
4: YELLOW_4,
3: YELLOW_3,
2: YELLOW_2,
1: YELLOW_1
}

CYAN_5 = (0, 255, 240)
CYAN_4 = (0, 235, 222)
CYAN_3 = (0, 220, 210)
CYAN_2 = (0, 200, 190)
CYAN_1 = (0, 180, 170)

cyan_shades = {
5: CYAN_5,
4: CYAN_4,
3: CYAN_3,
2: CYAN_2,
1: CYAN_1
}

PURPLE_5 = (240, 0, 255)
PURPLE_4 = (222, 0, 235)
PURPLE_3 = (210, 0, 220)
PURPLE_2 = (190, 0, 200)
PURPLE_1 = (170, 0, 180)

purple_shades = {
5: PURPLE_5,
4: PURPLE_4,
3: PURPLE_3,
2: PURPLE_2,
1: PURPLE_1
}

GREY_5 = (255, 255, 255)
GREY_4 = (215, 215, 215)
GREY_3 = (190, 190, 190)
GREY_2 = (150, 150, 150)
GREY_1 = (90, 90, 90)

grey_shades = {
5: GREY_5, 
4: GREY_4, 
3: GREY_3, 
2: GREY_2, 
1: GREY_1 
}

def get_shade(r, g, b):
    # primary
    if r > 0 and g == 0 and b == 0:
        return red_shades[r]
    elif r == 0 and g > 0 and b == 0:
        return green_shades[g]
    elif r == 0 and g == 0 and b > 0:
        return blue_shades[b]
        
    elif r > 0 and g > 0 and b == 0:
        shade = max((r, g))
        return yellow_shades[shade]
    elif r == 0 and g > 0 and b > 0:
        shade = max((g, b))
        return cyan_shades[shade]
    elif r > 0 and g == 0 and b > 0:
        shade = max((r, b))
        return purple_shades[shade]
        
    else:
        shade = max((r, g, b))
        return grey_shades[shade]