$(document).ready(function () {

    $('#create-avatar-video-form').validate({
        rules: {
            segment: {
                required: true
            },
            video_url: {
                required: true,
                url: true
            },
            avatar_id: {
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
            video_url: {
                required: "Video URL is required",
                url: "Please enter a valid URL"
            },
            avatar_id: {
                required: "Avatar ID is required"
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