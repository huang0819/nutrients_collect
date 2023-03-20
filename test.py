import matplotlib.pyplot as plt
import numpy as np


class RGBDData:
    def __init__(self, file):
        self.file = file
        self.image, self.depth, self.fx, self.fy = read_npz_file(file)


def read_npz_file(file):
    data = np.load(file)

    if 'rgb_image' in data.files and 'depth_image' in data.files:
        rgb_image = data['rgb_image']
        depth_image = data['depth_image'] * data.get('depth_scale', 1)
        fx = data.get('fx', 615.4642333984375)
        fy = data.get('fy', 615.4144897460938)

        return rgb_image, depth_image, fx, fy
    else:
        raise KeyError


class Tray:
    def __init__(self, file, process=None):
        self.data = RGBDData(file)
        self.process = process if process is not None else []

    def get_image(self):
        # to RGB
        return self.data.image[:, :, ::-1] if self.data else None

    def get_depth(self):
        return self.data.depth if self.data else None

    def show(self):
        fig = plt.figure(figsize=(8, 6))

        ax_1 = fig.add_subplot(121)
        ax_1.imshow(self.get_image())
        ax_1.axis('off')

        ax_2 = fig.add_subplot(122)
        ax_2.imshow(self.get_depth())
        ax_2.axis('off')

        plt.show()

    def preprocessed_depth(self):
        depth = self.get_depth()
        for p in self.process:
            depth = p['func'](depth, **p['param'])

        return depth


if __name__ == '__main__':
    tray = Tray(r"D:\Downloads\data_2023-03-19_2023-03-20\20230316164724.npz")
    tray.show()
