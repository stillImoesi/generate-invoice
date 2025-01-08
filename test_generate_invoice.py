# AI generated test cases for generate_invoice.py

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO
from datetime import datetime
from generate_invoice import seller_name, seller_address_line1, seller_address_line2, seller_country, seller_business_id, seller_vat_number, seller_bank_account, seller_swift
from generate_invoice import args, customer_number
from generate_invoice import args, customer_number
from generate_invoice import products
from generate_invoice import formatted_ref_number, pdf_output_path

from generate_invoice import (
    read_reference_number,
    write_reference_number,
    get_customer_number,
    read_last_customer_number,
    display_customers,
    select_or_create_customer,
    update_customer_number,
    validate_finnish_reference_number,
    generate_finnish_reference_number,
    PDF
)

class TestGenerateInvoice(unittest.TestCase):

    @patch('generate_invoice.os.getenv')
    def test_load_env_variables(self, mock_getenv):
        mock_getenv.side_effect = lambda key: {
            'SELLER_NAME': 'Test Seller',
            'SELLER_ADDRESS_LINE1': 'Test Address Line 1',
            'SELLER_ADDRESS_LINE2': 'Test Address Line 2',
            'SELLER_COUNTRY': 'Test Country',
            'SELLER_BUSINESS_ID': '1234567-8',
            'SELLER_VAT_NUMBER': 'FI12345678',
            'SELLER_BANK_ACCOUNT': 'FI00 1234 5600 0007 85',
            'SELLER_SWIFT': 'NDEAFIHH'
        }.get(key)
        
        
        self.assertEqual(seller_name, 'Test Seller')
        self.assertEqual(seller_address_line1, 'Test Address Line 1')
        self.assertEqual(seller_address_line2, 'Test Address Line 2')
        self.assertEqual(seller_country, 'Test Country')
        self.assertEqual(seller_business_id, '1234567-8')
        self.assertEqual(seller_vat_number, 'FI12345678')
        self.assertEqual(seller_bank_account, 'FI00 1234 5600 0007 85')
        self.assertEqual(seller_swift, 'NDEAFIHH')

    @patch('generate_invoice.input', side_effect=['1', 'Test Company', 'Test Street', '12345', 'Test City', 'FI12345678', 'Test Contact'])
    @patch('generate_invoice.display_customers', return_value=[])
    @patch('generate_invoice.select_or_create_customer', return_value=None)
    @patch('generate_invoice.get_customer_number', return_value=None)
    @patch('generate_invoice.read_last_customer_number', return_value=100)
    @patch('generate_invoice.update_customer_number')
    def test_create_new_corporate_customer(self, mock_update_customer_number, mock_read_last_customer_number, mock_get_customer_number, mock_select_or_create_customer, mock_display_customers, mock_input):
        test_args = ['generate_invoice.py']
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(customer_number, 101)
            mock_update_customer_number.assert_called_once()

    @patch('generate_invoice.input', side_effect=['0', 'Test Individual', 'test@example.com', 'Test Street', '12345', 'Test City'])
    @patch('generate_invoice.display_customers', return_value=[])
    @patch('generate_invoice.select_or_create_customer', return_value=None)
    @patch('generate_invoice.get_customer_number', return_value=None)
    @patch('generate_invoice.read_last_customer_number', return_value=100)
    @patch('generate_invoice.update_customer_number')
    def test_create_new_private_customer(self, mock_update_customer_number, mock_read_last_customer_number, mock_get_customer_number, mock_select_or_create_customer, mock_display_customers, mock_input):
        test_args = ['generate_invoice.py']
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(customer_number, 101)
            mock_update_customer_number.assert_called_once()

    @patch('generate_invoice.input', side_effect=['Test Product', '2', '100', '24'])
    def test_collect_products(self, mock_input):
        test_args = ['generate_invoice.py']
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0][0], 'Test Product')
            self.assertEqual(products[0][1], 2)
            self.assertAlmostEqual(products[0][2], 80.65, places=2)
            self.assertAlmostEqual(products[0][3], 19.35, places=2)
            self.assertEqual(products[0][4], 24)

    @patch('generate_invoice.input', side_effect=['2023-10-10', 'Test message'])
    @patch('generate_invoice.read_reference_number', return_value=1000)
    @patch('generate_invoice.write_reference_number')
    @patch('generate_invoice.generate_finnish_reference_number', return_value='1234567890')
    def test_generate_invoice(self, mock_generate_finnish_reference_number, mock_write_reference_number, mock_read_reference_number, mock_input):
        test_args = ['generate_invoice.py']
        with patch.object(sys, 'argv', test_args):
            self.assertEqual(formatted_ref_number, '1234567890')
            self.assertTrue(pdf_output_path.endswith('1234567890.pdf'))

if __name__ == '__main__':
    unittest.main()