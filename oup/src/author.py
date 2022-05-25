from dataclasses import dataclass                       
@dataclass
class Author:
    name:str

    @staticmethod
    def from_rssxml(parsed):
        return Author(name = parsed.get('name',''))
