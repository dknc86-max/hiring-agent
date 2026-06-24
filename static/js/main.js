document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('resume');
    const fileLabel = document.querySelector('.file-label-text');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileLabel.textContent = this.files[0].name;
            } else {
                fileLabel.textContent = 'Choose a PDF resume';
            }
        });
    }
});