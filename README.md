# Ragatex Product Update Web Application

A modern web application for updating product status based on inventory levels. The app processes CSV files containing SPU ID, price, and inventory data, performs vlookup operations, and generates two different Excel files for download.

## Features

- **Modern Web Interface**: Clean, responsive design with drag-and-drop file upload
- **CSV Processing**: Handles inventory files with SPU ID, price, and inventory columns
- **Vlookup Integration**: Automatically finds Product IDs for given SPU IDs
- **Dual File Generation**: Creates two Excel files for download:
  - **Product Status Update**: Updates product status based on inventory levels (Active/Inactive)
  - **Price Template**: Contains Product IDs with inventory > 0 and their prices
- **Excel Export**: Downloads both files in Excel format
- **Real-time Status**: System status monitoring and validation

## How It Works

1. **Upload CSV**: User uploads a CSV file with SPU ID, price, and inventory columns
2. **Vlookup SPU IDs**: System finds corresponding Product IDs using the vlookup database
3. **Generate Files**: System creates two Excel files:
   - **Product Status Update**: Updates product status based on inventory:
     - `inventory = 0` → Status = "Inactive"
     - `inventory > 0` → Status = "Active"
   - **Price Template**: Contains only products with inventory > 0, including Product ID, inventory, and price
4. **Download Files**: User receives both Excel files for download

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure required files are present**:
   - `vlookup_analysis_results.csv` (in project root)
   - `simple-price-template(1).xlsx` (Excel template for price file generation)
   - `product_status_updates/` folder with at least one status file

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5001
   ```

## File Structure

```
ragatex-product-update/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── vlookup_analysis_results.csv   # Vlookup database (required)
├── simple-price-template(1).xlsx  # Excel template for price file generation
├── example_inventory.csv          # Example CSV file format
├── product_status_updates/        # Product status files folder
│   └── *.csv                     # Status update files
├── uploads/                       # Temporary upload folder
├── templates/
│   ├── index.html                # Main HTML template
│   └── download.html             # Download page template
└── static/
    ├── css/
    │   └── style.css             # Modern CSS styles
    └── js/
        └── script.js             # JavaScript functionality
```

## CSV File Format

The uploaded CSV file must contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| SPU ID | Product SPU identifier | 1234567890123 |
| price | Product price | 29.99 |
| inventory | Stock quantity | 0 or 100 |

## API Endpoints

- `GET /` - Main application page
- `POST /upload` - File upload and processing
- `GET /download_files` - Download page with file links
- `GET /download/<file_type>` - Download specific file (main or price_template)
- `GET /api/status` - System status check

## System Requirements

- Python 3.7+
- Flask 2.3.3+
- pandas 2.1.1+
- openpyxl 3.1.2+

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Troubleshooting

### Common Issues

1. **"No product status update files found"**
   - Ensure the `product_status_updates/` folder exists
   - Add at least one CSV file with the format: `DD-MM-YY-product_status_update.csv`

2. **"Vlookup database not found"**
   - Ensure `vlookup_analysis_results.csv` exists in the project root

3. **File upload errors**
   - Check file size (max 10MB)
   - Ensure file is CSV format
   - Verify required columns are present

### Logs

Check the console output for detailed error messages and processing logs.

## Security Notes

- File uploads are validated for type and size
- Temporary files are cleaned up after processing
- No sensitive data is stored permanently

## License

© 2024 Ragatex Product Update System. All rights reserved.
