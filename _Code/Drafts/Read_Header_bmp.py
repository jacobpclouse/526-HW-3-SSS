# https://stackoverflow.com/questions/47003833/how-to-read-bmp-file-header-in-python
# WARNING: DeprecationWarning: 'imghdr' is deprecated and slated for removal in Python 3.13 for import imghdr

import imghdr

bitmap_filename = input("Please input the name of the file you want to get the header from: ")
print(imghdr.what(bitmap_filename))