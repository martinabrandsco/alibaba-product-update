from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import os
import tempfile
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ragatex_product_update_secret_key_2024'

# Simple demo data for Vercel (since we can't use the large CSV files)
DEMO_SPU_DATA = {
    '8445588433000': {'inventory': 12, 'price': 29.99, 'product_id': '1601488260019'},
    '8445484333428': {'inventory': 3, 'price': 15.50, 'product_id': '1601488262002'},
    '8718526121797': {'inventory': 4, 'price': 25.00, 'product_id': '1601488262001'},
    '603912303223': {'inventory': 5, 'price': 45.99, 'product_id': '1601488260017'},
    '714718001333': {'inventory': 4, 'price': 35.00, 'product_id': '1601488261008'},
    '603912349986': {'inventory': 20, 'price': 55.00, 'product_id': '1601488260016'},
    '603912746303': {'inventory': 60, 'price': 42.50, 'product_id': '1601488260006'},
    '8420327541116': {'inventory': 80, 'price': 55.00, 'product_id': '1601488259014'},
    '609224031618': {'inventory': 0, 'price': 28.99, 'product_id': '1601488260005'}
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing - Demo version for Vercel"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    # For demo purposes, we'll use the demo data instead of processing the actual file
    flash('Demo Mode: Using sample data instead of uploaded file (Vercel limitation)')
    
    # Store demo results in session
    from flask import session
    session['demo_mode'] = True
    session['processed_data'] = DEMO_SPU_DATA
    
    return render_template('download_demo.html', data=DEMO_SPU_DATA)

@app.route('/download_files')
def download_files():
    """Download page with links to both Excel files"""
    from flask import session
    if 'demo_mode' in session:
        return render_template('download_demo.html', data=session.get('processed_data', DEMO_SPU_DATA))
    return render_template('download.html')

@app.route('/download/<file_type>')
def download_file(file_type):
    """Download specific file type - Demo version"""
    from flask import session
    
    if file_type == 'main':
        # Create a simple demo Excel file
        import pandas as pd
        from io import BytesIO
        
        # Create demo data
        demo_data = []
        for spu_id, info in DEMO_SPU_DATA.items():
            status = "Active" if info['inventory'] > 0 else "Inactive"
            demo_data.append({
                'Product ID': info['product_id'],
                'SPU ID': spu_id,
                'Status': status,
                'Inventory': info['inventory'],
                'Price': info['price']
            })
        
        df = pd.DataFrame(demo_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Product Status', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=f"ragatex_product_update_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    elif file_type == 'price_template':
        # Create a simple demo price template
        import pandas as pd
        from io import BytesIO
        
        # Filter products with inventory > 0
        price_data = []
        for spu_id, info in DEMO_SPU_DATA.items():
            if info['inventory'] > 0:
                price_data.append({
                    'Identify ID': info['product_id'],
                    'Inventory': info['inventory'],
                    'Price': info['price']
                })
        
        df = pd.DataFrame(price_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Price Template', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=f"price_template_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    else:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint to check system status"""
    return jsonify({
        'status': 'demo_mode',
        'message': 'Running in demo mode on Vercel',
        'limitations': [
            'No persistent file storage',
            'Using demo data instead of uploaded files',
            'Limited to 10-second function timeout'
        ],
        'demo_data_available': len(DEMO_SPU_DATA),
        'platform': 'vercel'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "platform": "vercel",
        "timestamp": datetime.now().isoformat()
    })

# This is the entry point for Vercel
# Vercel will automatically call this when a request comes in
