// Registration Page JavaScript

// Toggle password visibility
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field.type === 'password') {
        field.type = 'text';
    } else {
        field.type = 'password';
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            // Check password match
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('❌ Passwords do not match!');
                return false;
            }
            
            // Check password length
            if (password.length < 8) {
                e.preventDefault();
                alert('❌ Password must be at least 8 characters!');
                return false;
            }
            
            // Show loading
            const btn = form.querySelector('.submit-btn');
            btn.disabled = true;
            btn.textContent = 'Registering... ⏳';
        });
    }
});

// Mobile number validation (only numbers)
document.addEventListener('DOMContentLoaded', function() {
    const mobileField = document.getElementById('mobile');
    if (mobileField) {
        mobileField.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
    }
});