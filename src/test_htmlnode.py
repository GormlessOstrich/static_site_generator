import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "href": "https://boot.dev"},)
        self.assertEqual(node.props_to_html(), ' class="greeting" href="https://boot.dev"',)

    def test_values(self):
        node = HTMLNode("div", "Hi.",)
        self.assertEqual(node.tag, "div",)
        self.assertEqual(node.value, "Hi.",)
        self.assertEqual(node.children, [],)
        self.assertEqual(node.props, {},)

    def test_repr(self):
        node = HTMLNode("p", "Hello.", [], {"class": "primary"},)
        self.assertEqual(node.__repr__(), "HTMLNode(p, Hello., [], {'class': 'primary'})",)

    # Leaf tests.

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # Parent tests.

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_multiple_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold."), LeafNode(None, "Plaintext."), LeafNode("i", "Italic."), LeafNode(None, "Plaintext."),],)
        self.assertEqual(node.to_html(), "<p><b>Bold.</b>Plaintext.<i>Italic.</i>Plaintext.</p>",)

    def test_headings(self):
        node = ParentNode("h2", [LeafNode("b", "Bold."), LeafNode(None, "Plaintext."), LeafNode("i", "Italic."), LeafNode(None, "Plaintext."),],)
        self.assertEqual(node.to_html(), "<h2><b>Bold.</b>Plaintext.<i>Italic.</i>Plaintext.</h2>",)

if __name__ == "__main__":
    unittest.main()