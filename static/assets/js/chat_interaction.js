// Handle chat interaction

$(document).ready(function() {
    $('#chat-form').submit(function(e) { // Assuming your form has an ID 'chat-form'
      e.preventDefault(); // Prevent default form submission
      $.ajax({
        url: '/get_response',
        type: 'POST',
        data: { question: $('#question-input').val() }, // Assuming 'question-input' is your input field's ID
        success: function(response) {
          // Update chat display
          $('#chat-history').append(`
            <div class="card my-3" style="border-color: var(--bs-body-color);border-width: 2px;">
              <div class="card-body">
                <h4 class="card-title"><img src="static/assets/img/photo-1561037404-61cd46aa615b.jpg">You</h4>
                <p class="card-text my-4">${response.response}</p> 
              </div>
            </div>
         `);
        }
      });
    });
  });