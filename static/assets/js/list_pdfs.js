

$(document).ready(function() {
    var fileListContainer = $('#file-list');
    var progressBar = $('#upload-progress-bar'); // Ensure you have this element in HTML

    $('input[type="file"]').on('change', function() {
        fileListContainer.empty(); // Clear existing entries
        progressBar.hide().find('.progress-bar').css('width', '0%').attr('aria-valuenow', 0); // Reset and hide progress bar
        var files = this.files; // Get the list of files
        if (files.length > 0) {
            $.each(files, function(i, file) {
                fileListContainer.append('<p class="mb-1 temp-file">' + file.name + ' <span class="text-muted">(Uploading...)</span></p>');
            });
            progressBar.show(); // Show progress bar when there are files
        } else {
            fileListContainer.html('<p>No files uploaded yet.</p>'); // Show default message if no file
        }
    });

    // Handle the form submission with AJAX
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        // AJAX call to server to upload files
        $.ajax({
            url: '/upload_pdf', // Adjust as necessary
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = evt.loaded / evt.total;
                        percentComplete = parseInt(percentComplete * 100);
                        progressBar.find('.progress-bar').css('width', percentComplete + '%').attr('aria-valuenow', percentComplete);
                    }
                }, false);
                return xhr;
            },
            success: function(data) {
                console.log('Upload successful');
                $('.temp-file').find('span.text-muted').text('(Ready)');
            },
            error: function() {
                console.error('Error uploading files');
                $('.temp-file').find('span.text-muted').text('(Failed to upload)');
            },
            complete: function() {
                progressBar.hide(); // Hide the progress bar on completion
            }
        });
    });
});

