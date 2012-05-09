import sys, os
sys.path.append(os.path.split(os.path.abspath(__file__))[0])

import unittest
import tempfile
import subprocess
from functools import partial
from utils import convert_utils
from pyPdf import PdfFileReader


class TestPDFUtils(unittest.TestCase):

    def setUp(self):
        self.HTML = "<html><body><h1>Hello World!</h1></body></html>"

    def test_convert_mac(self):
        import platform
        self.assertEqual(platform.system(), 'Darwin',
                            'Machine has to be a mac to test')
        convert_utils.create_PDF = convert_utils.convert_mac

        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        try:
            with open(temppdffile_path, 'wb') as fp:
                fp.write(convert_utils.create_PDF(self.HTML))
            output = subprocess.check_output('file %s' % temppdffile_path,
                                                                shell=True)
            self.assertNotEqual(output.find('PDF document'), -1)
        finally:
            os.unlink(temppdffile_path)

    def test_convert_wkhtmltopdf(self):
        wkhtmltopdf_path = subprocess.check_output('which wkhtmltopdf',
                                                    shell=True).rstrip()
        convert_utils.create_PDF = partial(convert_utils.convert_wkhtmltopdf,
                                            wkhtmltopdf_path=wkhtmltopdf_path)

        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        try:
            with open(temppdffile_path, 'wb') as fp:
                fp.write(convert_utils.create_PDF(self.HTML))
            output = subprocess.check_output('file %s' % temppdffile_path,
                                                                shell=True)
            self.assertNotEqual(output.find('PDF document'), -1)
        finally:
            os.unlink(temppdffile_path)

    def test_pdktk_write_PDF_encrypted(self):
        pdftk_path = subprocess.check_output('which pdftk',
                                                    shell=True).rstrip()
        convert_utils.write_PDF = partial(convert_utils.pdktk_write_PDF,
                                                    pdftk_path=pdftk_path)

        pdf_data = convert_utils.create_PDF(self.HTML)
        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        convert_utils.write_PDF(temppdffile_path, pdf_data)
        with open(temppdffile_path, 'rb') as fp:
            pdfReaderObj = PdfFileReader(fp)
            self.assertTrue(pdfReaderObj.isEncrypted)
        os.unlink(temppdffile_path)

    def test_reportlab_write_PDF_encrypted(self):
        # Assuming reportlab and rlextra will be installed by default
        # and automatically imported
        convert_utils.write_PDF = convert_utils.reportlab_write_PDF

        pdf_data = convert_utils.create_PDF(self.HTML)
        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        convert_utils.write_PDF(temppdffile_path, pdf_data)
        with open(temppdffile_path, 'rb') as fp:
            pdfReaderObj = PdfFileReader(fp)
            self.assertTrue(pdfReaderObj.isEncrypted)
        os.unlink(temppdffile_path)

    def test_pdktk_write_PDF_unencrypted(self):
        pdftk_path = subprocess.check_output('which pdftk',
                                                    shell=True).rstrip()
        convert_utils.write_PDF = partial(convert_utils.pdktk_write_PDF,
                                                    pdftk_path=pdftk_path)

        pdf_data = convert_utils.create_PDF(self.HTML)
        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        convert_utils.write_PDF(temppdffile_path, pdf_data, encrypted=False)
        with open(temppdffile_path, 'rb') as fp:
            pdfReaderObj = PdfFileReader(fp)
            self.assertFalse(pdfReaderObj.isEncrypted)
        os.unlink(temppdffile_path)

    def test_reportlab_write_PDF_unencrypted(self):
        #Assuming reportlab and rlextra will be installed by default
        # and automatically imported
        convert_utils.write_PDF = convert_utils.reportlab_write_PDF

        pdf_data = convert_utils.create_PDF(self.HTML)
        temppdffile = tempfile.NamedTemporaryFile(suffix='.pdf')
        temppdffile_path = temppdffile.name
        temppdffile.close()

        convert_utils.write_PDF(temppdffile_path, pdf_data, encrypted=False)
        with open(temppdffile_path, 'rb') as fp:
            pdfReaderObj = PdfFileReader(fp)
            self.assertFalse(pdfReaderObj.isEncrypted)
        os.unlink(temppdffile_path)

if __name__ == '__main__':
    unittest.main()
