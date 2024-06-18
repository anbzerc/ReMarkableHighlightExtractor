import os
import argparse
import cv2
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

def add_page_number(page, page_num):
    rect = page.rect
    text = f"Page {page_num}"
    page.insert_text((10, 10), text, fontsize=12, fontname="helv")  # Position (10, 10), font size 12

def extractHighlightedPages(highlighted, output, start, end, numbering, display, blanks):
    if start != 0 and numbering == 1:
        start -= 1

    scale = 5
    mat = fitz.Matrix(scale, scale)

    highlightedPages = fitz.open(highlighted)
    writer = PdfWriter()

    for i in range(start + (numbering - 1), end):
        print(f"Processing page {i + 1}...")
        highlightedPage = highlightedPages.load_page(i)
        highlightedPix = highlightedPage.get_pixmap(matrix=mat)
        highlightedPix.save('highlightedPage.jpg')

        img = cv2.imread('highlightedPage.jpg')

        # Set yellow range
        yellowRange = [(20, 100, 100), (30, 255, 255)]  # You might need to adjust these values
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv, yellowRange[0], yellowRange[1])
        yellow_detected = cv2.countNonZero(yellow_mask) > 0

        if yellow_detected:
            # Add page number to the highlighted page
            add_page_number(highlightedPage, i + 1)

            # Convert the highlighted page to a PDF page and add to the writer
            temp_pdf_path = 'temp_page.pdf'
            pdf_page = fitz.open()  # Create a new PDF in memory
            pdf_page.insert_pdf(highlightedPages, from_page=i, to_page=i)
            pdf_page.save(temp_pdf_path)

            temp_pdf_reader = PdfReader(temp_pdf_path)
            writer.add_page(temp_pdf_reader.pages[0])

            if display:
                cv2.imshow('image', img)
                cv2.waitKey(0)

            os.remove(temp_pdf_path)

        else:
            if display and blanks:
                cv2.imshow('image', img)
                cv2.waitKey(0)

        os.remove('highlightedPage.jpg')

    with open(output, 'wb') as outputStream:
        writer.write(outputStream)

    highlightedPages.close()

def main(args):
    end = args.end

    if end == 0:
        reader = PdfReader(args.highlighted)
        end = len(reader.pages)

    extractHighlightedPages(args.highlighted, args.output, args.start, end, args.numbering, args.display, args.blanks)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract pages with yellow highlights from a PDF.")
    parser.add_argument('highlighted', help="path of highlighted PDF")
    parser.add_argument('output', help="path of output PDF file")
    parser.add_argument('-s', '--start', help="extraction starting page", default=0, type=int)
    parser.add_argument('-e', '--end', help="extraction ending page", default=0, type=int)
    parser.add_argument('-n', '--numbering', help="the page relative to the PDF file where the page numbering actually starts at 1", default=1, type=int)
    parser.add_argument('-d', '--display', help="display the image of the page", action='store_true')
    parser.add_argument('-b', '--blanks', help="display the image of the page even if no highlights were detected", action='store_true')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)
