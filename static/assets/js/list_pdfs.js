

$(document).ready(function() {
    $('input[type="file"]').on('change', function() {
        var fileListContainer = $('#file-list');
        fileListContainer.empty(); // Clear existing entries

        var files = this.files; // Get the list of files
        if (files.length > 0) {
            $.each(files, function(i, file) {
                fileListContainer.append('<p class="mb-1"><span style="text-decoration: underline;">' + file.name + '</span></p>');
            });
        } else {
            fileListContainer.html('<p>No files uploaded yet.</p>'); // Show default message if no file
        }
    });

    // Optional: Handle the form submission here if needed
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        // AJAX call to server to upload files
        $.ajax({
            url: '/upload_pdf',  // Adjust as necessary
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                console.log('Upload successful');
                // Update UI or alert user
            },
            error: function() {
                console.error('Error uploading files');
            }
        });
    });
});
