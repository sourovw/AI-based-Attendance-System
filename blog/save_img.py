import os
import secrets
from PIL import Image
from flask_login import current_user
from blog import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    try:
        os.chdir('./blog/static/faces/')
        os.mkdir(current_user.username)
    except Exception as e:
        print(e)

    img_dir = './static/faces/' + current_user.username
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, img_dir, picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
