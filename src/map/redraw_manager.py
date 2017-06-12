

class RedrawManager(object):

    def __init__(self, map):

        self.map = map

    def run(self):

        if not self.map.color_map.needs_recompute():
            return

        redraw = self.map.color_map.recompute_maps()
        if not redraw:
            return

        self.map.map_image.add_batch_to_redraw(redraw)
        self.map.map_image.redraw_tiles()
