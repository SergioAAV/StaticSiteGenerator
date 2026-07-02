from textnode import TextNode, TextType


def main() -> None:
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test)


main()
