// Scripts personalizados para la aplicación de notas DIAN

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions (if needed in future)
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || '¿Está seguro de que desea eliminar este elemento?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Initialize date inputs with current date if empty
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });

    // Initialize time inputs with current time if empty
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        if (!input.value) {
            const now = new Date();
            const timeString = now.toTimeString().split(' ')[0].substring(0, 5);
            input.value = timeString;
        }
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButtons = form.querySelectorAll('button[type="submit"]');
            submitButtons.forEach(button => {
                button.disabled = true;
                const originalText = button.innerHTML;
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Cargando...';
                // Restore after 10 seconds as fallback
                setTimeout(() => {
                    button.disabled = false;
                    button.innerHTML = originalText;
                }, 10000);
            });
        });
    });

    // Table row highlighting
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    console.log('Scripts de notas DIAN cargados correctamente');
});