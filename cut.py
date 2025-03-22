from PIL import Image, ImageSequence

def crop_gif(input_path, output_path, top_crop=20, bottom_crop=20):
    """
    
    :param input_path: 
    :param output_path: 
    :param top_crop: 
    :param bottom_crop: 
    """
    img = Image.open(input_path)

    frames = []
    for frame in ImageSequence.Iterator(img):
        cropped_frame = frame.crop((0, top_crop, img.width, img.height - bottom_crop))
        frames.append(cropped_frame)

    frames[0].save(output_path, save_all=True, append_images=frames[1:])

if __name__ == "__main__":
    crop_gif("static/cropped_animation_NEW.gif", "static/cropped_animation_NEW2.gif")
