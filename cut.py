from PIL import Image, ImageSequence

def crop_gif(input_path, output_path, top_crop=20, bottom_crop=20):
    """
    قص الحواف الزائدة من الأعلى والأسفل فقط وحفظ الصورة الجديدة.
    
    :param input_path: مسار الصورة الأصلية
    :param output_path: مسار حفظ الصورة الجديدة
    :param top_crop: مقدار القص من الأعلى (بالبكسل)
    :param bottom_crop: مقدار القص من الأسفل (بالبكسل)
    """
    img = Image.open(input_path)

    # ✅ إذا كانت الصورة GIF متحركة، عالج جميع الإطارات
    frames = []
    for frame in ImageSequence.Iterator(img):
        cropped_frame = frame.crop((0, top_crop, img.width, img.height - bottom_crop))
        frames.append(cropped_frame)

    # ✅ حفظ الصورة الجديدة في مسار مختلف
    frames[0].save(output_path, save_all=True, append_images=frames[1:])

# ✅ تشغيل القص وحفظ الصورة في مسار جديد
if __name__ == "__main__":
    crop_gif("static/cropped_animation_NEW.gif", "static/cropped_animation_NEW2.gif")