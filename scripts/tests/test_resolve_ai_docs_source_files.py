import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "resolve-ai-docs-source-files.py"
SPEC = importlib.util.spec_from_file_location("resolve_ai_docs_source_files", SCRIPT_PATH)
resolver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)


class ResolveAiDocsSourceFilesTest(unittest.TestCase):
    def test_normalize_image_ref_resolves_deep_relative_path(self):
        self.assertEqual(
            resolver.normalize_image_ref(
                "ai/integrations/vector-search/doc.md",
                "../../media/image.png",
            ),
            "ai/media/image.png",
        )

    def test_normalize_image_ref_resolves_absolute_repo_path(self):
        self.assertEqual(
            resolver.normalize_image_ref("ai/doc.md", "/media/foo.png"),
            "media/foo.png",
        )

    def test_normalize_image_ref_strips_query_and_fragment(self):
        self.assertEqual(
            resolver.normalize_image_ref("ai/doc.md", "images/foo.png?v=2#section"),
            "ai/images/foo.png",
        )

    def test_normalize_image_ref_handles_angle_brackets(self):
        self.assertEqual(
            resolver.normalize_image_ref("ai/doc.md", "<../media/foo.png>"),
            "media/foo.png",
        )

    def test_normalize_image_ref_handles_spaces_in_path(self):
        self.assertEqual(
            resolver.normalize_image_ref("ai/doc.md", "images/path with spaces/image.png"),
            "ai/images/path with spaces/image.png",
        )

    def test_normalize_image_ref_handles_optional_title(self):
        self.assertEqual(
            resolver.normalize_image_ref("ai/doc.md", 'images/foo.png "title"'),
            "ai/images/foo.png",
        )

    def test_normalize_image_ref_ignores_external_images(self):
        self.assertIsNone(
            resolver.normalize_image_ref("ai/doc.md", "<https://example.com/foo.png>")
        )

    def test_images_from_markdown_finds_reference_style_images(self):
        content = """
![Inline](./inline.png)
![Reference image][diagram]
![Collapsed reference][]

[diagram]: ../media/diagram.svg "Diagram"
[Collapsed reference]: /media/collapsed.webp
"""
        self.assertEqual(
            resolver.images_from_markdown("ai/guide/doc.md", content),
            {
                "ai/guide/inline.png",
                "ai/media/diagram.svg",
                "media/collapsed.webp",
            },
        )

    def test_normalize_requested_files_treats_images_as_repo_relative(self):
        self.assertEqual(
            resolver.normalize_requested_files(
                "media/diagram.png, vector-search.md, overview.png",
                "ai",
                "TOC-ai.md",
            ),
            ["media/diagram.png", "ai/vector-search.md", "overview.png"],
        )


if __name__ == "__main__":
    unittest.main()
