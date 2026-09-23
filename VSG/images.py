#!/bin/env python
import os
import VSG
from mimetypes import guess_type

class Images:

    __gallery__  = None
    __realpath__ = ""
    __subdir__   = ""
    __dir_list__ = []
    __img_list__ = []

    def __init__(self, gallery: VSG.gallery.Gallery, subdirectory: str):
        if type(gallery) is not VSG.gallery.Gallery:
            raise ValueError("A valid gallery must be providd")
        self.__gallery__ = gallery
        self.__realpath__ = os.path.join(self.__gallery__.path, subdirectory)
        self.__subdir__ = subdirectory

    def GetList(self):
        directories = os.listdir(self.__realpath__)
        for item in directories:
            newItem = VSG.gallery.GalleryItem(self.__gallery__, os.path.join(self.__subdir__, item))
            if newItem.isdir == True:
                self.__dir_list__.append(newItem)
            else:
                mtype = guess_type(item)
                if mtype is not None and mtype[0].lower().startswith("image/"):
                    self.__img_list__.append(newItem)

        return (self.__dir_list__ + self.__img_list__).sort()

    def GetListImages(self):
        if len(self.__img_list__) + len(self.__dir_list__) == 0:
            self.GetList()

        return self.__img_list__.sort()

    def GetListDirectories(self):
        if len(self.__img_list__) + len(self.__dir_list__) == 0:
            self.GetList()

        return self.__dir_list__.sort()

    def __str__(self):
        return f"<Images:{self.__realpath__}>"
