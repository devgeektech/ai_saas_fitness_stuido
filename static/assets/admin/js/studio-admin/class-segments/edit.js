$(document).ready(function () {

    $('#edit-class-segment-form').validate({

        rules: {

            class_obj: {
                required: true
            },

            exercise: {
                required: true
            },

            segment_type: {
                required: true
            },

            title: {
                required: true
            },

            script: {
                required: true
            },

            order: {
                required: true,
                number: true,
                min: 1
            },

            duration: {
                required: true,
                number: true,
                min: 1
            }
        },

        messages: {

            class_obj: {
                required: "Class is required"
            },

            exercise: {
                required: "Exercise is required"
            },

            segment_type: {
                required: "Segment type is required"
            },

            title: {
                required: "Title is required"
            },

            script: {
                required: "Script is required"
            },

            order: {
                required: "Order is required",
                number: "Please enter a valid number",
                min: "Order must be greater than 0"
            },

            duration: {
                required: "Duration is required",
                number: "Please enter a valid number",
                min: "Duration must be greater than 0"
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