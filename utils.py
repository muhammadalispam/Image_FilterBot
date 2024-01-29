from PIL import Image, ImageFilter

filters = [
    'BLUR',
    'EMBOSS',
    'CONTOUR',
    'DETAIL',
    'EDGE_ENHANCE',
    'EDGE_ENHANCE_MORE',
    'FIND_EDGES',
    'SHARPEN',
    'SMOOTH',
    'SMOOTH_MORE',
]


async def filter_user_image(filename, filter):
    img1 = Image.open(filename)
    for f in filters:
        if f == filter:
            filtered_image = img1.filter(eval(f"ImageFilter.{filter}"))
            filtered_image.save(filename)



