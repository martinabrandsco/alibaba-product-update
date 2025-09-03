from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ragatex_product_update_secret_key_2024'

# Simple demo data for Vercel
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

# Simple HTML template embedded in the code
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ragatex Product Update - Demo Mode</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .demo-notice { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 20px 0; color: #856404; }
        .btn { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }
        .btn:hover { background: #0056b3; }
        .btn-secondary { background: #28a745; }
        .btn-secondary:hover { background: #1e7e34; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #f8f9fa; }
        .status-active { color: green; font-weight: bold; }
        .status-inactive { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Ragatex Product Update</h1>
            <p>Demo Mode - Running on Vercel</p>
        </div>
        
        <div class="demo-notice">
            <strong>⚠️ Demo Mode Notice:</strong> This is running on Vercel with limitations. 
            For full functionality with file uploads, deploy to Railway or DigitalOcean instead.
        </div>
        
        <h2>📁 Download Demo Files</h2>
        <p>Sample data has been processed. You can download demo Excel files:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="/download/main" class="btn">📥 Download Demo Product Status File</a>
            <a href="/download/price_template" class="btn btn-secondary">📥 Download Demo Price Template</a>
        </div>
        
        <h3>📊 Demo Data Preview</h3>
        <table>
            <thead>
                <tr>
                    <th>SPU ID</th>
                    <th>Product ID</th>
                    <th>Inventory</th>
                    <th>Price</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for spu_id, info in data.items() %}
                <tr>
                    <td>{{ spu_id }}</td>
                    <td>{{ info.product_id }}</td>
                    <td>{{ info.inventory }}</td>
                    <td>${{ "%.2f"|format(info.price) }}</td>
                    <td>
                        <span class="{% if info.inventory > 0 %}status-active{% else %}status-inactive{% endif %}">
                            {% if info.inventory > 0 %}Active{% else %}Inactive{% endif %}
                        </span>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/" class="btn">🔄 Refresh</a>
            <a href="/api/status" class="btn">📊 API Status</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page with demo data"""
    return render_template_string(HTML_TEMPLATE, data=DEMO_SPU_DATA)

@app.route('/download/<file_type>')
def download_file(file_type):
    """Download demo files"""
    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file
        
        if file_type == 'main':
            # Create demo product status data
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
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Product Status', index=False)
            output.seek(0)
            
            return send_file(
                output,
                as_attachment=True,
                download_name=f"ragatex_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        elif file_type == 'price_template':
            # Create demo price template data
            price_data = []
            for spu_id, info in DEMO_SPU_DATA.items():
                if info['inventory'] > 0:
                    price_data.append({
                        'Identify ID': info['product_id'],
                        'Inventory': info['inventory'],
                        'Price': info['price']
                    })
            
            df = pd.DataFrame(price_data)
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
            return jsonify({"error": "Invalid file type"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'demo_mode',
        'message': 'Running in demo mode on Vercel',
        'platform': 'vercel',
        'demo_data_count': len(DEMO_SPU_DATA),
        'timestamp': datetime.now().isoformat(),
        'limitations': [
            'No persistent file storage',
            'Using demo data instead of uploaded files',
            'Limited to 10-second function timeout'
        ]
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