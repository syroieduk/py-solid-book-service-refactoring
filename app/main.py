import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class Display(ABC):
    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplay(Display):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplay(Display):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class Printer(ABC):
    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ElementTree.Element("book")
        title = ElementTree.SubElement(root, "title")
        title.text = book.title
        content = ElementTree.SubElement(root, "content")
        content.text = book.content
        return ElementTree.tostring(root, encoding="unicode")


DISPLAYS = {"console": ConsoleDisplay, "reverse": ReverseDisplay}
PRINTERS = {"console": ConsolePrinter, "reverse": ReversePrinter}
SERIALIZERS = {"json": JsonSerializer, "xml": XmlSerializer}


def create(registry: dict, key: str, kind: str) -> None:
    if key not in registry:
        raise ValueError(f"Unknown {kind} type: {key}")
    return registry[key]()


def run_display(book: Book, method_type: str) -> None:
    create(DISPLAYS, method_type, "display").display(book)


def run_print(book: Book, method_type: str) -> None:
    create(PRINTERS, method_type, "print").print_book(book)


def run_serialize(book: Book, method_type: str) -> str:
    return create(SERIALIZERS, method_type, "serialize").serialize(book)


ACTIONS = {"display": run_display, "print": run_print}


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "serialize":
            return run_serialize(book, method_type)
        action = ACTIONS.get(cmd)
        if action:
            action(book, method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
