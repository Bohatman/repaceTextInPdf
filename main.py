# import pdfminer
# from PyPDF2 import PdfFileWriter
# import pdfplumber
# pdf_writer = PdfFileWriter()
# with pdfplumber.open(r'Exercise Book Version 5.5.0-v1.1.0_PDFRemovePassword3049.pdf') as pdf:
#     first_page = pdf.pages[0]
#     print(type(first_page))
#     print(first_page.chars)
#     for i in range(len(first_page.chars)):
#         first_page.chars[i]['text'] = "asds"
#         print(first_page.chars[i])
#     first_page.to_image().save("e.png")
#
from PyPDF4.generic import ByteStringObject
from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_


def remove_watermark(input_file, output_file):
    with open(input_file, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]
                    if isinstance(text, ByteStringObject):
                        operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(output_file, "wb") as outputStream:
            output.write(outputStream)


inputFile = r'in.pdf'
outputFile = r"out.pdf"
remove_watermark(inputFile, outputFile)
