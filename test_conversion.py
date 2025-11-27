import unittest
import os
import csv
from vuln_converter import txt_to_csv, csv_to_txt

class TestVulnConverter(unittest.TestCase):
    def setUp(self):
        self.test_txt = "test_vuln.txt"
        self.test_csv = "test_vuln.csv"
        self.output_txt = "output_vuln.txt"
        self.output_csv = "output_vuln.csv"

    def tearDown(self):
        # Clean up temporary files
        for f in [self.test_txt, self.test_csv, self.output_txt, self.output_csv]:
            if os.path.exists(f):
                os.remove(f)

    def test_txt_to_csv_conversion(self):
        # Create dummy TXT
        with open(self.test_txt, 'w') as f:
            f.write("react@16.8.0\n")
            f.write("@angular/core@12.0.0\n") # Scoped package
            f.write("lodash@4.17.21")

        # Run conversion
        txt_to_csv(self.test_txt, self.output_csv)

        # Verify CSV content
        with open(self.output_csv, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            self.assertEqual(rows[0], ['package', 'version'])
            self.assertEqual(rows[1], ['react', '16.8.0'])
            self.assertEqual(rows[2], ['@angular/core', '12.0.0'])
            self.assertEqual(rows[3], ['lodash', '4.17.21'])

    def test_csv_to_txt_conversion(self):
        # Create dummy CSV
        with open(self.test_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['package', 'version'])
            writer.writerow(['axios', '0.21.1'])
            writer.writerow(['@types/node', '14.14.31'])

        # Run conversion
        csv_to_txt(self.test_csv, self.output_txt)

        # Verify TXT content
        with open(self.output_txt, 'r') as f:
            lines = f.readlines()
            self.assertIn("axios@0.21.1\n", lines)
            self.assertIn("@types/node@14.14.31\n", lines)

    def test_round_trip_integrity(self):
        # Data -> TXT -> CSV -> TXT -> Check Data
        original_data = ["express@4.17.1\n", "@vue/cli@4.5.0\n"]
        
        with open(self.test_txt, 'w') as f:
            f.writelines(original_data)
        
        txt_to_csv(self.test_txt, self.output_csv)
        csv_to_txt(self.output_csv, self.output_txt)
        
        with open(self.output_txt, 'r') as f:
            final_data = f.readlines()
        
        self.assertEqual(original_data, final_data)

if __name__ == '__main__':
    unittest.main()
