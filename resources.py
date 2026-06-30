import json
import os.path
from typing import List


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path: str = data_path
        self.entries: List[Entry] = list()

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_path, filename)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for item in value.get('entries', []):
            sub_entry = cls.from_json(item)
            entry.add_entry(sub_entry)
        return entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            content = json.load(f)
        print(type(content))
        return cls.from_json(content)

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            # 'entries': [x.json() for x in self.entries]
            'entries': []
        }
        for entry in self.entries:
            res['entries'].append(entry.json())
        return res

    def save(self, path):
        entry_json_dict = self.json()
        final_path = os.path.join(path, f'{self.title}.json')
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(entry_json_dict, f, ensure_ascii=False)


def print_with_indent(value, indent=0):
    leaf = "\t" * indent
    print(leaf + str(value))


def entry_from_json(value: dict) -> Entry:
    entry = Entry(value['title'])
    for item in value.get('entries', []):
        sub_entry = entry_from_json(item)
        entry.add_entry(sub_entry)
    return entry
