import argparse
import io
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def compress_pdf(input_path, output_path, dpi, quality, mode):
    source = fitz.open(input_path)
    output = fitz.open()

    if mode == "color":
        colorspace = fitz.csRGB
        pil_mode = "RGB"
    elif mode == "grayscale":
        colorspace = fitz.csGRAY
        pil_mode = "L"
    else:
        raise ValueError("Mode must be 'color' or 'grayscale'")

    for page in source:
        scale = dpi / 72
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(scale, scale),
            colorspace=colorspace,
            alpha=False
        )

        image = Image.frombytes(
            pil_mode,
            (pixmap.width, pixmap.height),
            pixmap.samples
        )

        jpeg_buffer = io.BytesIO()
        image.save(
            jpeg_buffer,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        new_page = output.new_page(
            width=page.rect.width,
            height=page.rect.height
        )

        new_page.insert_image(
            new_page.rect,
            stream=jpeg_buffer.getvalue()
        )

    output.save(
        output_path,
        garbage=4,
        clean=True,
        deflate=True
    )

    output.close()
    source.close()

    size = Path(output_path).stat().st_size
    print(f"Created: {output_path}")
    print(f"Size: {size:,} bytes ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compress a scanned PDF while choosing color and quality."
    )

    parser.add_argument("input", help="Input PDF")
    parser.add_argument("output", help="Output PDF")

    parser.add_argument(
        "--mode",
        choices=["color", "grayscale"],
        default="color",
        help="Keep color or convert to grayscale. Default: color"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=180,
        help="Rendering resolution. Default: 180"
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=75,
        help="JPEG quality from 1 to 95. Default: 75"
    )

    args = parser.parse_args()

    if not 1 <= args.quality <= 95:
        parser.error("quality must be between 1 and 95")

    compress_pdf(
        args.input,
        args.output,
        args.dpi,
        args.quality,
        args.mode
    )
