from fileposition import FilePosition
from typing import Tuple, Generator, TextIO

import os
import syntax
import copy
import codecs


class FileWalker:
    topdir: str  # Python uses strings for representing file names.

    def __init__(self, topdir):
        self.topdir = topdir  # No checks here.

    def recDirIterator(self) -> Generator[Tuple[str, str, FilePosition], None, None]:
        if os.path.exists(self.topdir) and os.path.isdir(self.topdir):
            for iter_dir in os.walk(self.topdir):
                for ktr in iter_dir[2]:
                    for tuple_cont in self.fileIterator(open(os.path.join(iter_dir[0], ktr), "r", encoding="utf8")):
                        yield os.path.join(iter_dir[0], ktr), tuple_cont[0], tuple_cont[1]
        else:
            raise OSError

    @staticmethod
    def fileIterator(f: TextIO) -> Generator[Tuple[str, FilePosition], None, None]:
        filepos = FilePosition()
        word_build = ""
        col_count = 1

        for chrt in f.read():
            if syntax.inWord(chrt):
                word_build += chrt
                if len(word_build) == 1:
                    filepos.column = col_count
            else:
                if len(word_build) > 0:
                    filepos_copy = copy.copy(filepos)
                    yield word_build, filepos_copy
                    word_build = ""
                if syntax.isNewLine(chrt):
                    filepos.nextLine()
                    col_count = 0
            col_count += 1

        if len(word_build) > 0:
            filepos_copy = copy.copy(filepos)
            yield word_build, filepos_copy
        f.close()

    def __repr__(self) -> str:
        return "FileWalker: " + self.topdir

    def __str__(self) -> str:
        return "FileWalker: " + self.topdir
