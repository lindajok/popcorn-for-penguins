# https://www.riff.ie/2020/02/05/wildcard-searching-trie.html
# https://github.com/TeodorDyakov/wildcard-trie/blob/master/src/trie/Trie.java
# https://gist.github.com/shehabic/5a004258793d7cf8cfa0ca15ffebb6a1

from typing import Dict, List, Any

WILDCARD = '?'

class Trie:
    def __init__(self):
        self.children : Dict[str, Trie] = {}
        self.isLeaf: bool = False

    def insert(self, word: str) -> None:
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.isLeaf = True

    def find(self, word: str) -> bool:
        stack = [(self, 0, '')]
        result = []

        while stack:
            curr, count, currWord = stack.pop()

            if count == len(word):
                if curr.isLeaf: result.append(currWord)
                continue

            currChar = word[count]
            if currChar == WILDCARD:
                for childChar, node in curr.children.items():
                    stack.append((node, count + 1, currWord + childChar))
                continue

            if currChar in curr.children:
                node = curr.children[currChar]
                stack.append((node, count + 1, currWord + currChar))

        return result

def main():
    trie = Trie()
    trie.insert('word')
    trie.insert('ward')
    trie.insert('oi')
    trie.insert('boi')
    
    print(trie.find('??'))
    assert(trie.find('??') == ['oi'])
    assert(trie.find('') == [])
    assert(trie.find('w?rd') == ['ward', 'word'])
    assert(trie.find('???') == ['boi'])
    assert(trie.find('?oi') == ['boi'])

if __name__ == '__main__':
    main()
