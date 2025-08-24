import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_links, extract_markdown_images, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word.", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This is text with a ", TextType.PLAINTEXT), TextNode("bold", TextType.BOLD), TextNode(" word.", TextType.PLAINTEXT),], new_nodes,)

    def test_delimiter_two_bold_sections(self):
        node = TextNode("This is text with a **bold** word and **another.**", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This is text with a ", TextType.PLAINTEXT), TextNode("bold", TextType.BOLD), TextNode(" word and ", TextType.PLAINTEXT), TextNode("another.", TextType.BOLD),], new_nodes,)

    def test_delimiter_multiple_bold_words(self):
        node = TextNode("This is text with a **bold word** and **another.**", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([TextNode("This is text with a ", TextType.PLAINTEXT), TextNode("bold word", TextType.BOLD), TextNode(" and ", TextType.PLAINTEXT), TextNode("another.", TextType.BOLD),], new_nodes,)

    def test_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word.", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual([TextNode("This is text with an ", TextType.PLAINTEXT), TextNode("italic", TextType.ITALIC), TextNode(" word.", TextType.PLAINTEXT),], new_nodes,)

    def test_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([TextNode("bold", TextType.BOLD), TextNode(" and ", TextType.PLAINTEXT), TextNode("italic", TextType.ITALIC),], new_nodes,)

    def test_delimiter_code(self):
        node = TextNode("This is text with a `code block`.", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual([TextNode("This is text with a ", TextType.PLAINTEXT), TextNode("code block", TextType.CODE), TextNode(".", TextType.PLAINTEXT),], new_nodes,)

    # Regex tests.

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)")
        self.assertListEqual([("link", "https://boot.dev"), ("another link", "https://blog.boot.dev"),], matches,)

    # Image and link splitting tests.

    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAINTEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.PLAINTEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),], new_nodes,)

    def test_split_single_image(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.PLAINTEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),], new_nodes,)

    def test_split_multiple_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAINTEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with an ", TextType.PLAINTEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.PLAINTEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),], new_nodes,)

    def test_split_multiple_links(self):
        node = TextNode("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text afterwards.", TextType.PLAINTEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with a ", TextType.PLAINTEXT), TextNode("link", TextType.LINK, "https://boot.dev"), TextNode(" and ", TextType.PLAINTEXT), TextNode("another link", TextType.LINK, "https://blog.boot.dev"), TextNode(" with text afterwards.", TextType.PLAINTEXT),], new_nodes,)

    # text_to_textnodes tests.

    def test_delimiter_bold_and_italic(self):
        node = TextNode("**Bold** and _italic._", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual([TextNode("Bold", TextType.BOLD), TextNode(" and ", TextType.PLAINTEXT), TextNode("italic.", TextType.ITALIC),], new_nodes,)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is a **bold word** with an _italic word_, a `code block`, an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertListEqual([TextNode("This is a ", TextType.PLAINTEXT), TextNode("bold word", TextType.BOLD), TextNode(" with an ", TextType.PLAINTEXT), TextNode("italic word", TextType.ITALIC), TextNode(", a ", TextType.PLAINTEXT), TextNode("code block", TextType.CODE), TextNode(", an ", TextType.PLAINTEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and a ", TextType.PLAINTEXT), TextNode("link", TextType.LINK, "https://boot.dev"),], nodes,)

if __name__ == "__main__":
    unittest.main()