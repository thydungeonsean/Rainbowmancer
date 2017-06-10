from color import add_colors


def set_shade_scale(r=0, g=0, b=0, step=-45):

    shades = {}

    i = 5
    for s in range(250, (250 + (step*5)), step):

        if r < 0:
            sr = s
        else:
            sr = r
        if g < 0:
            sg = s
        else:
            sg = g
        if b < 0:
            sb = s
        else:
            sb = b

        shades[i] = (sr, sg, sb)

        i -= 1

    return shades

red_shades = set_shade_scale(-1, 10)

green_shades = set_shade_scale(25, -1)

blue_shades = set_shade_scale(20, 0, -1)

# yellow_shades = set_shade_scale(-1, -1, 20)

# cyan_shades = set_shade_scale(0, -1, -1)

# purple_shades = set_shade_scale(-1, 15, -1)

grey_shades = set_shade_scale(-1, -1, -1)

purple_shades = {}
for i in range(1, 6):
    purple_shades[i] = add_colors(red_shades[i], blue_shades[i])

yellow_shades = {}
for i in range(1, 6):
    yellow_shades[i] = add_colors(red_shades[i], green_shades[i])

cyan_shades = {}
for i in range(1, 6):
    cyan_shades[i] = add_colors(green_shades[i], blue_shades[i])


def col_mod_shade(shade, col_mod):

    mod_shade = shade + col_mod
    if mod_shade > 5:
        mod_shade = 5

    return mod_shade


def get_shade(r, g, b, col_mod):  # TODO make col_mod effect

    if r == 0 and g == 0 and b == 0:
        shade = 1
        hue = grey_shades
        return hue[shade]

    # primary
    elif r > 0 and g == 0 and b == 0:
        shade = r
        hue = red_shades
    elif r == 0 and g > 0 and b == 0:
        shade = g
        hue = green_shades
    elif r == 0 and g == 0 and b > 0:
        shade = b
        hue = blue_shades

    elif r > 0 and g > 0 and b == 0:
        shade = max((r, g))
        hue = yellow_shades
    elif r == 0 and g > 0 and b > 0:
        shade = max((g, b))
        hue = cyan_shades
    elif r > 0 and g == 0 and b > 0:
        shade = max((r, b))
        hue = purple_shades

    else:
        shade = max((r, g, b))
        hue = grey_shades

    return hue[col_mod_shade(shade, col_mod)]
