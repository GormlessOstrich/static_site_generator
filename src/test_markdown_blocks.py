import unittest
from markdown_blocks import markdown_to_blocks, markdown_to_html_node, block_to_block_type, BlockType

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is a **bold** paragraph.

This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a **bold** paragraph.", "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.", "- This is a list\n- with items",],)

    def test_markdown_to_blocks_newlines(self):
        markdown = """
This is a **bold** paragraph.




This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["This is a **bold** paragraph.", "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.", "- This is a list\n- with items",],)

# block_to_block_types tests.

    def test_block_to_block_types(self):
        block = "# A heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\nSome code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> A\n> multi-line quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- An unordered list\n- A list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. An ordered list\n2. A list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "A paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

#

    def test_paragraph(self):
        markdown = """
This is a **bold** paragraph.
There is some text in a p
tag here.

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bold</b> paragraph. There is some text in a p tag here.</p></div>",)

    def test_paragraphs(self):
        markdown = """
This is a **bold** paragraph.
There is some text in a p
tag here.

There is also another paragraph with _italic_ text and a `code block` here.

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bold</b> paragraph. There is some text in a p tag here.</p><p>There is also another paragraph with <i>italic</i> text and a <code>code block</code> here.</p></div>",)

    def test_lists(self):
        markdown = """
- This is an unordered list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is an unordered list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",)

    def test_headings(self):
        markdown = """
# This is a heading using the h1 tag

This is a paragraph.

## This is another heading using the h2 tag
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading using the h1 tag</h1><p>This is a paragraph.</p><h2>This is another heading using the h2 tag</h2></div>",)

    def test_blockquote(self):
        markdown = """
> This is a
> blockquote block.

This is a paragraph.

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a blockquote block.</blockquote><p>This is a paragraph.</p></div>",)

    def test_code(self):
        markdown = """
```
This is text that _should_ remain
the **same** despite its inline formatting.
```
"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>This is text that _should_ remain\nthe **same** despite its inline formatting.\n</code></pre></div>",)

if __name__ == "__main__":
    unittest.main()