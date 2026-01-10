// School Management System - Main JavaScript

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm delete actions
document.querySelectorAll('form[onsubmit*="confirm"]').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });
});

// Filter sections based on selected class
function filterSections(classId, sectionSelectId) {
    const sectionSelect = document.getElementById(sectionSelectId);
    if (!sectionSelect) return;
    
    const options = sectionSelect.querySelectorAll('option[data-class]');
    const selectedValue = sectionSelect.value;
    
    // Clear existing options except the first one
    sectionSelect.innerHTML = '<option value="">Select Section</option>';
    
    options.forEach(function(option) {
        const optionClassId = option.getAttribute('data-class');
        if (!classId || optionClassId == classId) {
            const newOption = option.cloneNode(true);
            sectionSelect.appendChild(newOption);
        }
    });
    
    // Restore selected value if it's still valid
    if (selectedValue && document.querySelector(`#${sectionSelectId} option[value="${selectedValue}"]`)) {
        sectionSelect.value = selectedValue;
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Loading...';
    element.disabled = true;
}

// Hide loading spinner
function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// Validate file upload
function validateFileUpload(input, maxSize = 16777216) { // 16MB default
    const file = input.files[0];
    if (!file) {
        alert('Please select a file.');
        return false;
    }
    
    if (file.size > maxSize) {
        alert(`File size exceeds the maximum limit of ${formatFileSize(maxSize)}.`);
        input.value = '';
        return false;
    }
    
    return true;
}

// Mark all attendance
function markAll(status) {
    document.querySelectorAll('input[type="radio"][value="' + status + '"]').forEach(function(radio) {
        radio.checked = true;
    });
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize popovers
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});
