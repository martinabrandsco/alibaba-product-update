// Ragatex Product Update - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    checkSystemStatus();
    setupFormValidation();
}

// File Upload Functionality
function setupFileUpload() {
    const fileInput1 = document.getElementById('fileInput1');
    const fileInput2 = document.getElementById('fileInput2');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadForm = document.getElementById('uploadForm');
    
    // Track which files are selected
    let inventoryFileSelected = false;
    let statusFileSelected = false;

    // File input change handlers
    fileInput1.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (validateFile(file, 'inventory')) {
                updateFileDisplay(fileInput1, file);
                inventoryFileSelected = true;
                checkBothFilesSelected();
                showFlashMessage('Inventory file selected successfully!', 'success');
            }
        } else {
            resetFileDisplay(fileInput1);
            inventoryFileSelected = false;
            checkBothFilesSelected();
        }
    });

    fileInput2.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (validateFile(file, 'status')) {
                updateFileDisplay(fileInput2, file);
                statusFileSelected = true;
                checkBothFilesSelected();
                showFlashMessage('Product status file selected successfully!', 'success');
            }
        } else {
            resetFileDisplay(fileInput2);
            statusFileSelected = false;
            checkBothFilesSelected();
        }
    });

    function validateFile(file, type) {
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showFlashMessage(`Please select a CSV file for ${type}.`, 'error');
            return false;
        }

        // Validate file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            showFlashMessage(`File size must be less than 10MB for ${type}.`, 'error');
            return false;
        }

        return true;
    }

    function updateFileDisplay(input, file) {
        const label = input.nextElementSibling;
        const text = label.querySelector('.file-input-text');
        const hint = label.querySelector('.file-input-hint');
        
        text.textContent = file.name;
        hint.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
    }

    function resetFileDisplay(input) {
        const label = input.nextElementSibling;
        const text = label.querySelector('.file-input-text');
        const hint = label.querySelector('.file-input-hint');
        
        if (input.id === 'fileInput1') {
            text.textContent = 'Choose Inventory CSV File';
        } else {
            text.textContent = 'Choose Product Status CSV File';
        }
        hint.textContent = 'or drag and drop here';
    }

    function checkBothFilesSelected() {
        uploadBtn.disabled = !(inventoryFileSelected && statusFileSelected);
    }

    // Drag and drop functionality
    fileInputLabel.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileInputLabel.style.borderColor = '#667eea';
        fileInputLabel.style.background = '#f0f4ff';
    });

    fileInputLabel.addEventListener('dragleave', function(e) {
        e.preventDefault();
        fileInputLabel.style.borderColor = '#ddd';
        fileInputLabel.style.background = '#fafafa';
    });

    fileInputLabel.addEventListener('drop', function(e) {
        e.preventDefault();
        fileInputLabel.style.borderColor = '#ddd';
        fileInputLabel.style.background = '#fafafa';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    // Form submission handler
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const inventoryFile = fileInput1.files[0];
        const statusFile = fileInput2.files[0];
        
        if (!inventoryFile || !statusFile) {
            showFlashMessage('Please select both files first.', 'error');
            return;
        }

        // Show loading state
        showLoadingState();
        
        // Use fetch to upload both files
        const formData = new FormData();
        formData.append('inventory_file', inventoryFile);
        formData.append('status_file', statusFile);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Check if response contains download page HTML
                return response.text().then(html => {
                    if (html.includes('Download Your Files') || html.includes('download-section')) {
                        // Replace the current page content with the download page
                        document.open();
                        document.write(html);
                        document.close();
                    } else {
                        // Reload page to show any error messages
                        window.location.reload();
                    }
                });
            } else {
                throw new Error('Upload failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFlashMessage('An error occurred while processing the files.', 'error');
            hideLoadingState();
        });
    });
}

// System Status Check
function checkSystemStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateStatusIndicator('vlookupStatus', data.vlookup_file_exists);
            updateStatusIndicator('productStatusFiles', data.product_status_folder_exists && data.most_recent_file);
            updateStatusIndicator('uploadSystem', data.upload_folder_exists);
        })
        .catch(error => {
            console.error('Error checking system status:', error);
            updateStatusIndicator('vlookupStatus', false);
            updateStatusIndicator('productStatusFiles', false);
            updateStatusIndicator('uploadSystem', false);
        });
}

function updateStatusIndicator(elementId, isOk) {
    const indicator = document.getElementById(elementId);
    if (isOk) {
        indicator.className = 'status-indicator success';
        indicator.innerHTML = '<i class="fas fa-check"></i>';
    } else {
        indicator.className = 'status-indicator error';
        indicator.innerHTML = '<i class="fas fa-times"></i>';
    }
}

// Form Validation
function setupFormValidation() {
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Disable upload button initially
    uploadBtn.disabled = true;
}

// Loading State Management
function showLoadingState() {
    const uploadBtn = document.getElementById('uploadBtn');
    const btnText = uploadBtn.querySelector('span');
    const loadingSpinner = uploadBtn.querySelector('.loading-spinner');
    
    uploadBtn.disabled = true;
    btnText.textContent = 'Processing...';
    loadingSpinner.style.display = 'block';
}

function hideLoadingState() {
    const uploadBtn = document.getElementById('uploadBtn');
    const btnText = uploadBtn.querySelector('span');
    const loadingSpinner = uploadBtn.querySelector('.loading-spinner');
    
    uploadBtn.disabled = false;
    btnText.textContent = 'Process File';
    loadingSpinner.style.display = 'none';
}

// Form Reset
function resetForm() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInputText = document.querySelector('.file-input-text');
    const fileInputHint = document.querySelector('.file-input-hint');
    
    fileInput.value = '';
    fileInputText.textContent = 'Choose CSV File';
    fileInputHint.textContent = 'or drag and drop here';
    uploadBtn.disabled = true;
}

// Flash Message System
function showFlashMessage(message, type = 'info') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const flashMessage = document.createElement('div');
    flashMessage.className = `flash-message flash-${type}`;
    
    const icon = type === 'error' ? 'exclamation-triangle' : 
                 type === 'success' ? 'check-circle' : 'info-circle';
    
    flashMessage.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button class="flash-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    flashContainer.appendChild(flashMessage);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (flashMessage.parentElement) {
            flashMessage.remove();
        }
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showFlashMessage('An unexpected error occurred. Please refresh the page.', 'error');
});

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Future: Register service worker for offline functionality
    });
}

