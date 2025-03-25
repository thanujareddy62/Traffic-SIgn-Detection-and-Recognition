$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Trigger image preview on file input change
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict using fetch API
    $('#btn-predict').click(async function () {
        // Create form data from the form element
        var formData = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        try {
            // Make POST request using fetch
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData,
            });

            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Parse the JSON response
            const data = await response.json();

            // Display the result
            $('.loader').hide();
            $('#result').fadeIn(600);
            $('#result').text(data.prediction || 'Prediction received!');
            console.log('Success!', data);
        } catch (error) {
            // Handle errors
            $('.loader').hide();
            $('#result').fadeIn(600);
            $('#result').text('Error occurred: ' + error.message);
            console.error('Error:', error);
        }
    });
});

