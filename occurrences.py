from fileposition import FilePosition
from typing import List, Dict, Set, Optional


class Occurrences:
    occs: Dict[str, Dict[str, Set[FilePosition]]]

    def __init__(self):
        self.occs = dict()

    def add(self, word: str, filename: str, pos: FilePosition) -> None:
        word = word.lower()
        if word not in self.occs:
            self.occs[word] = {filename: {pos}}
        elif word in self.occs and self.occs[word].__contains__(filename):
            self.occs[word][filename].add(pos)
        else:
            self.occs[word][filename] = {pos}


    # Should return the number of distinct words:

    def distinctWords(self) -> int:
        return len(self.occs)

    # Should return the total number of words occurrences:

    def totalOccurrences(self, word: Optional[str] = None,
                         fname: Optional[str] = None) -> int:
        tot = 0
        if word is None and fname is None:
            for keys in self.occs:
                for keysIn in self.occs[keys]:
                    tot += len(self.occs[keys][keysIn])
        elif fname is None and self.occs.__contains__(word.lower()):
            for keysIn in self.occs[word.lower()]:
                tot += len(self.occs[word.lower()][keysIn])
        elif not self.occs.__contains__(word.lower()) or not self.occs[word.lower()].__contains__(fname):
            return 0
        elif self.occs[word.lower()][fname]:
            return len(self.occs[word.lower()][fname])
        return tot

    # This is for debugging, so it doesn't need to be pretty:

    def __repr__(self) -> str:
        return str(self.occs)

    # Here the occurrences must be sorted and shown in a nice way:

    def __str__(self) -> str:
        str1 = ""
        key_list = list()
        for keys in self.occs:
            key_list.append(keys)
        key_list.sort()
        for keys in key_list:
            str1 += "\"" + keys + "\" has " + str(self.totalOccurrences(keys)) + " occurrences(s):\n"
            out = sorted(self.occs.get(keys).keys())
            for keysIn in out:
                str1 += "   in file " + str(keysIn) + "\n"
                sorrr = sorted(self.occs.get(keys).get(keysIn))
                for file_pos in sorrr:
                    str1 += "      at " + str(file_pos) + "\n"
        return str1
