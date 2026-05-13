$(document).ready(function (e) {
    e.preventDefault()
    // jQuery validation setup
    $('#create-class-form').validate({

        rules: {
            title: {
                required: true
            },
            category: {
                required: true
            },
            difficulty: {
                required: true
            },
            focus: {
                required: true
            },
            duration: {
                required: true,
                number: true,
                min: 1
            },
            status: {
                required: true
            }
        },

        messages: {
            title: {
                required: "Title is required"
            },
            category: {
                required: "Category is required"
            },
            difficulty: {
                required: "Difficulty is required"
            },
            focus: {
                required: "Focus is required"
            },
            duration: {
                required: "Duration is required",
                number: "Please enter a valid number",
                min: "Duration must be greater than 0"
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