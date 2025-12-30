from PIL import Image, ImageFilter, ImageEnhance


with Image.open('Capture.png') as pic:
    pic.show()

    saturate = ImageEnhance.Color(pic)
    saturate = saturate.enhance(1.2)
    # saturate.show()

    black_white = pic.convert('L')
    black_white.save('black_white.png')
    # black_white.show()

    mirror = pic.transpose(Image.FLIP_LEFT_RIGHT)
    # mirror.show()

    blur = pic.filter(ImageFilter.BLUR)
    # blur.show()

    #Image enhance
    color = ImageEnhance.Color(pic)
    color = color.enhance(1.2)
    color.save('color.png')

    contrast = ImageEnhance.Contrast(pic).enhance(2.5)
    contrast.save('contrast.png')