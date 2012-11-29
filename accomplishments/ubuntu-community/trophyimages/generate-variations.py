#!/usr/bin/python
import os
import Image
import ImageEnhance

def generate_icon_variations():

    images_path = "."

    lock_image_path = os.path.join("special", "lock.png")
    lockimage = Image.open(lock_image_path)
    for name in os.listdir(images_path):
        try:
        
            orig_filename = os.path.join(images_path, name)
            orig_filecore = os.path.splitext(orig_filename)[0]
            orig_filetype = os.path.splitext(orig_filename)[1]
            
            if os.path.isdir(orig_filename):
                continue # Skip directories
                
            if orig_filetype == ".py":
                continue # Do not configure this script's file
                
            if orig_filecore.split("-")[-1] in ["locked","opportunity", "opportunity_auto","locked_auto"]:
                # Don't ever try to make -locked-locked-locked... images.
                continue
        
            im = Image.open(orig_filename)

            # Opacity set to 1.0 until we figure out a better way of
            # showing opportunities
            reduced = _create_reduced_opacity_trophy_icon(im,
                                                               1.0)
            reduced.save(orig_filecore + "-opportunity_auto" + orig_filetype)

            if im.mode != 'RGBA':
                im = im.convert('RGBA')
            layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
            position = (
                im.size[0] - lockimage.size[0], im.size[1] - lockimage.size[1])
            layer.paste(lockimage, position)
            img = Image.composite(layer, reduced, layer)
            img.save(orig_filecore + "-locked_auto" + orig_filetype)

        except Exception, (msg):
            print msg

def _create_reduced_opacity_trophy_icon( im, opacity):
    """Returns an image with reduced opacity."""

    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

if __name__ == "__main__":
    generate_icon_variations()
