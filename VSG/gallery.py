#!/bin/env python
import os
import functools

@functools.total_ordering
class GalleryItem:

    subpath = ""
    realpath = ""
    basename = ""
    isdir = False

    def __init__(self, gallery: VSG.gallery.Gallery, subpath: str):
        if gallery is None:
            raise ValueError("Gallery cannot be none")

        if subpath is None or subpath == "":
            raise ValueError("Subpath must be set")

        self.realpath = os.path.realpath(os.path.join(gallery.path, subpath))

        if self.realpath.startswith(gallery.path) == False or self.realpath == gallery.path:
            raise ValueError(f"The subpath '{self.realpath}' must be a subpath of '{gallery.path}'")

        self.isdir = os.path.isdir(self.realpath)

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

@functools.total_ordering
class Gallery:
    name = ""
    path = ""
    icon = ""

    def __init__(self, name = "", path = "", icon = ""):
        if path is None:
            raise ValueError("Path cannot be empty")

        if os.path.isdir(path) == False:
            raise ValueError(f"Path don't exists : {path}")

        self.path = os.path.realpath(path)

        if name is None or name.strip() == "":
            self.name = os.path.basename(path)

        self.icon = icon

    def __str__(self):
        return f"<Gallery:{self.path}>"

    def __lt__(self, other):
        if other is not GalleryItem:
            return NotImplemented

        return self.name < other.name or (self.name == other.name and self.path < other.path)

    def __eq__(self, other):
        if other is not GalleryItem:
            return NotImplemented

        return self.name == other.name and self.path == other.path
