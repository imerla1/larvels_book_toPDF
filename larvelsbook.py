import ssl
from urllib.request import urlretrieve
from fpdf import FPDF


ssl._create_default_https_context = ssl._create_unverified_context

http = "https://img.yumpu.com/54479513/{}/983x1270/learning-laravels-eloquent.jpg?quality=100"
print("download is starting please wait . . . . ")


def download(url):
    for k in range(0, 200):
        name = '{}.jpg'.format(k)

        urlretrieve(url.format(k), name)
        print(name, "is Downloading ...")


download(http)

print("Download successfully Completed !!!")
question = str(input("Do you want to save images as PDF file y or n"))
if question == "n":
    print("Ok Buy, Buy")

if question == 'y':
    print("Please weight a few seconds")
    pdf = FPDF()
    for i in range(200):
        pdf.add_page()
        pdf.image("{}.jpg".format(i), x=10, y=8, w=220, h=320)
    pdf.output("Larvlebook.pdf")


