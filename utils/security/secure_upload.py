from os.path import join
from werkzeug.utils import secure_filename
from uuid import uuid4
from PIL import Image


def secure_image_uploader(form, file_path):

    try:
        filename = secure_filename(form.image.data.filename)
    except AttributeError:
        raise Exception("Form must be a flask web form and not a different type")

    image_id = str(uuid4())
    new_filename = image_id + '.png'

    file_img_path = join(file_path, new_filename)
    form.image.data.save(file_img_path)

    return file_img_path, image_id
