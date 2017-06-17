

class RedrawManager(object):

    def __init__(self, map):

        self.map = map
        self.fov_redraw_list = []

    def set_fov_redraw(self, fov):
        self.fov_redraw_list.extend(fov)

    def run(self):

        if self.map.color_map.needs_recompute():

            color_list = self.map.color_map.recompute_maps()
            self.map.map_image.add_batch_to_redraw(color_list)
        else:
            color_list = False

        if self.fov_redraw_list:
            self.map.map_image.add_batch_to_redraw(self.fov_redraw_list)

        if self.fov_redraw_list or color_list:

            self.map.map_image.redraw_tiles()

            del self.fov_redraw_list[:]
