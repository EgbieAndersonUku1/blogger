from PIL import Image
from os.path import exists, join, dirname


class ImageSize(object):

    HUNDRED_PIXELS = ("sm", 100)
    TWO_HUNDRED_PIXELS = ("sm", 200)
    THREE_HUNDRED_PIXELS = ("sm", 300)
    FOUR_HUNDRED_PIXELS = ("sm", 400)
    FIVE_HUNDRED_PIXELS = ("sm", 500)
    SIX_HUNDRED_PIXELS = ("lg", 600)
    SEVEN_HUNDRED_PIXELS = ("lg", 700)
    EIGHT_HUNDRED_PIXELS = ("lg", 800)
    NINE_HUNDRED_PIXELS = ("lg", 900)
    THOUSAND_PIXELS =  ("lg", 1000)


class Imager(object):

    def __init__(self, file_path, image_id, img_size):
        self._file_path = file_path
        self._image_id = image_id
        self.img_size = img_size

        if not exists(self._file_path):
            raise FileNotFoundError("The file directory was not found")

    def resize(self):

        img_size_type, new_img_size = self.img_size

        image = Image.open(self._file_path)
        height = self._calculate_image_dimensions_for_new_image_size(image, new_img_size)

        image = image.resize((new_img_size, height), Image.ANTIALIAS)

        new_img_ext = f'.{img_size_type}.png'
        new_img_path = self._create_file_path(extenstion=new_img_ext)

        image.save(new_img_path)

    def _calculate_image_dimensions_for_new_image_size(self, image, new_img_size):

        width_percent = (new_img_size / float(image.size[0]))
        height = int((float(image.size[1] * float(width_percent))))
        return height

    def _create_file_path(self, extenstion):
        directory_path = dirname(self._file_path)
        return join(directory_path, self._image_id + extenstion)


def resize_post_image(file_path, image_id, image_size):

    img = Imager(file_path, image_id, image_size)
    img.resize()
