#!/bin/env python
import os
from VSG.gallery import GalleryItem, Gallery
from mimetypes import guess_type

class Images:
    def __init__(self, gallery: Gallery, subdir: str):
        if type(gallery) is not Gallery:
            raise ValueError("A valid gallery must be provided")

        self.gallery = gallery
        self.realpath = os.path.join(self.gallery.path, subdir)
        self.subdir = subdir
        self.__dir_list__ = []
        self.__img_list__ = []

    def GetList(self):
        if ((self.__dir_list__ is None or len(self.__dir_list__) == 0) and
            (self.__img_list__ is None or len(self.__img_list__) == 0)):
            directories = os.listdir(self.realpath)
            for item in directories:
                newItem = GalleryItem(self.gallery, os.path.join(self.subdir, item))
                if newItem.isdir == True:
                    self.__dir_list__.append(newItem)
                else:
                    mtype = guess_type(item)
                    if mtype is not None:
                        if mtype[0] is not None and mtype[0].lower().startswith("image/"):
                            self.__img_list__.append(newItem)

            self.__img_list__.sort()
            self.__dir_list__.sort()

        # Folder first, then files
        return self.__dir_list__ + self.__img_list__

    def GetListImages(self):
        if len(self.__img_list__) + len(self.__dir_list__) == 0:
            self.GetList()

        return self.__img_list__

    def GetListDirectories(self):
        if len(self.__img_list__) + len(self.__dir_list__) == 0:
            self.GetList()

        return self.__dir_list__

    def __str__(self):
        return f"<Images:{self.realpath}>"
