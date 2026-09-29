#!/bin/env python
import os
import functools
from mimetypes import guess_type
from flask import url_for
from PIL import Image, ImageOps
from pathlib import Path

default_width = 300

@functools.total_ordering
class Gallery:
    def __init__(self, name = "", path = "", icon = ""):
        if path is None:
            raise ValueError("Path cannot be empty")

        if os.path.isdir(path) == False:
            raise ValueError(f"Path don't exists : {path}")

        self.path = os.path.realpath(path)

        if name is None or name.strip() == "":
            self.name = os.path.basename(path)
        else:
            self.name = name

        self.icon = icon

    def __str__(self):
        return f"<Gallery:{self.path}>"

    def __lt__(self, other):
        if other is not Gallery:
            return NotImplemented

        return self.name < other.name or (self.name == other.name and self.path < other.path)

    def __eq__(self, other):
        if other is not Gallery:
            return NotImplemented

        return self.name == other.name and self.path == other.path

@functools.total_ordering
class GalleryItem:
    def __init__(self, gallery: Gallery, subpath: str):
        if gallery is None:
            raise ValueError("Gallery cannot be none")

        if subpath is None or subpath == "":
            raise ValueError("Subpath must be set")

        self.realpath = os.path.realpath(os.path.join(gallery.path, subpath))

        if self.realpath.startswith(gallery.path) == False or self.realpath == gallery.path:
            raise ValueError(f"The subpath '{self.realpath}' must be a subpath of '{gallery.path}'")

        self.isdir = os.path.isdir(self.realpath)
        self.gallery = gallery
        self.subpath = subpath
        self.basename = os.path.basename(subpath)

    def __str__(self):
        return f"<GalleryItem:{self.realpath}>"

    def __lt__(self, other):
        if type(other) is not GalleryItem:
            raise NotImplementedError()

        return self.realpath < other.realpath

    def __eq__(self, other):
        if type(other) is not GalleryItem:
            raise NotImplementedError()

        return self.realpath == other.realpath

    def GetThumb(self, width=default_width):
        thumbPath = "html/static/icons/file.svg" if self.isdir == False else "html/static/icons/folder.svg"

        if self.IsImage() == True:
            thumbPath = os.path.realpath(os.path.join("cache", str(width) + "px", self.gallery.name, self.subpath))
            if os.path.exists(thumbPath) == False:
                self.GenerateThumb(thumbPath=thumbPath, isImageChecked=True, width=width)

        return thumbPath

    def GetFile(self):
        return self.realpath

    def GetThumbUrl(self, width: int=default_width):
        return url_for("get_file_thumbnail", w=width, gallery = self.gallery.name, subpath = self.subpath or ".")

    def GetUrl(self):
        return url_for("get_file", gallery = self.gallery.name, subpath = self.subpath or "." )

    def GenerateThumb(self, thumbPath, isImageChecked=False, width=default_width):
        # Don't generate if exists or not an image
        if self.IsImage() == False or os.path.exists(thumbPath):
            return

        with Image.open(self.realpath) as img:
            resized_img = ImageOps.exif_transpose(img)
            w, h = resized_img.size
            new_w = width
            new_h = int(h * new_w / w)
            resized_img = resized_img.resize((new_w, new_h), Image.BICUBIC)
            os.makedirs(os.path.dirname(thumbPath), exist_ok=True)
            resized_img.save(thumbPath)

    def IsImage(self):
        if self.isdir == True:
            return False

        mtype = guess_type(self.realpath)
        return mtype is not None and mtype[0] is not None and mtype[0].startswith("image/")

    def NameWithoutExtension(self):
        return Path(self.basename).stem
