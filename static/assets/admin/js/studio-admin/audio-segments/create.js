$(document).ready(function () {

    $('#create-audio-segment-form').validate({

        rules: {

            segment: {
                required: true
            },

            audio_url: {
                required: true,
                url: true
            },

            duration: {
                required: true,
                number: true,
                min: 1
            },

            voice_id: {
                required: true
            },

            status: {
                required: true
            }
        },

        messages: {

            segment: {
                required: "Segment is required"
            },

            audio_url: {
                required: "Audio URL is required",
                url: "Please enter a valid URL"
            },

            duration: {
                required: "Duration is required",
                number: "Please enter a valid number",
                min: "Duration must be greater than 0"
            },

            voice_id: {
                required: "Voice ID is required"
            },

            status: {
                required: "Status is required"
            }
        },

        errorElement: 'div',

        errorClass: 'text-danger',

        highlight: function (element) {

            $(element).addClass('is-invalid');
        },

        unhighlight: function (element) {

            $(element).removeClass('is-invalid');
        },

        submitHandler: function (form) {

            form.submit();
        }
    });

});