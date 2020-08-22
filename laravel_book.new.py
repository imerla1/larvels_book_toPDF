import requests
import os
from fpdf import FPDF
from PIL import Image
import threading
import re

# Total pages [1 - 222]

base_url = 'https://img.yumpu.com/54479513/{}/983x1270/learning-laravels-eloquent.jpg?quality=100'

all_urls = [base_url.format(page) for page in range(1, 222)] # All image urls

pdf = FPDF()

def atoi(text):
    return int(text) if text.isdigit() else text

def image_sorter(text):
    # Sort image Names ascending order
    # 0.jpg, 1jpg ...
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def download_images(urls_arry):
    # TODO use threads ??
    name_template = "{}.jpg"
    counter = 0
    for url in urls_arry:
        print("Downloading image from %s" % url)
        print('Image Name - %s' % name_template.format(counter))
        resp = requests.get(url)
        imageData = resp.content
        with open(name_template.format(counter), 'wb') as ff:
            ff.write(imageData)
        print("Image Download succesfully")
        counter += 1
    print("Downloading Proces --------- finished!")
def clear_directory():
    _listdir = os.listdir()
    for each in _listdir:
        if each.endswith(".jpg"):
            os.remove(each)


images = [image for image in os.listdir(os.getcwd()) if image.endswith('.jpg')]
sorted_images = images.sort(key=image_sorter)
def create_pdf(output_file_name='test.pdf'):
    images = [image for image in os.listdir(os.getcwd()) if image.endswith('.jpg')]
    sorted_images = sorted(images, key=image_sorter)
    print("-------------- we are Building PDF FOR YOU PLEASE W8 -------------------")
    for image in sorted_images:
        print("Mergin %s into pdf file" % image)
        cover = Image.open(image)
        width, height = cover.size
        # convert pixel in mm with 1px=0.264583 mm
        width, height = float(width * 0.264583), float(height * 0.264583)
        # given we are working with A4 format size 
        pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

        # get page orientation from image size
        orientation = "P" if width < height else "L"
        #  make sure image size is not greater than the pdf format size
        width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
        pdf.add_page(orientation=orientation)
        pdf.image(image, 0, 0, width, height)

    pdf.output(output_file_name, 'F')
    print("---------------- PDF proccessing FINISHED !!!! you can read your book")

# download_images(all_urls)
if __name__ == "__main__":
    main_thread = threading.Thread(target=download_images, args=[all_urls])
    main_thread.start()
    main_thread.join()
    create_pdf()
    clear_directory()
    os.system('xdg-open test.pdf')