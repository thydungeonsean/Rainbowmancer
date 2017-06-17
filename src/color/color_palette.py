from color import add_colors, boost_color, drain_color


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

white_shades = set_shade_scale(-1, -1, -1)
white_shades[0] = (30, 30, 30)

purple_shades = {}
for i in range(1, 6):
    purple_shades[i] = add_colors(red_shades[i], blue_shades[i])
    purple_shades[i] = boost_color(purple_shades[i], 25)

yellow_shades = {}
for i in range(1, 6):
    yellow_shades[i] = add_colors(red_shades[i], green_shades[i])
    yellow_shades[i] = boost_color(yellow_shades[i], 40)

#print yellow_shades

cyan_shades = {}
for i in range(1, 6):
    cyan_shades[i] = add_colors(green_shades[i], blue_shades[i])
    cyan_shades[i] = boost_color(cyan_shades[i], 50)


hue_key = {
    0: white_shades,
    1: red_shades,
    2: green_shades,
    3: blue_shades,
    4: yellow_shades,
    5: purple_shades,
    6: cyan_shades
}


hue_enmities = {
    0: {},
    1: {3, 6},
    2: {1, 5},
    3: {2, 4},
    4: {5},
    5: {6},
    6: {4}
}


def col_mod_shade(shade, col_mod):

    mod_shade = shade + col_mod
    if mod_shade > 5:
        mod_shade = 5

    return mod_shade


def get_shade(r, g, b, col_mod, reflected=False, seen=True):

    if r == 0 and g == 0 and b == 0:
        if reflected:
            shade = 4
        elif seen:
            shade = 1
        else:
            shade = 0
        hue = white_shades
        return hue[shade]

    elif seen:
        # primary
        if r > 0 and g == 0 and b == 0:
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
            hue = white_shades
    else:
        shade = 1
        hue = white_shades
        return hue[shade]

    return hue[col_mod_shade(shade, col_mod)]


def get_hue(r, g, b):
    if r == 0 and g == 0 and b == 0:
        return 0
    # primary
    elif r > 0 and g == 0 and b == 0:
        return 1
    elif r == 0 and g > 0 and b == 0:
        return 2
    elif r == 0 and g == 0 and b > 0:
        return 3
    # secondary
    elif r > 0 and g > 0 and b == 0:
        return 4
    elif r > 0 and g == 0 and b > 0:
        return 5
    elif r == 0 and g > 0 and b > 0:
        return 6
    # white
    else:
        return 0


def hue_interaction(object_hue, tile_hue):

    if object_hue == tile_hue and object_hue != 0:
        return 'positive'
    elif tile_hue in hue_enmities[object_hue]:
        return 'negative'
    else:
        return None
