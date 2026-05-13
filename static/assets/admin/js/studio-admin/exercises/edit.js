$(document).ready(function () {
    $('#edit-exercise-form').validate({
        rules: {
            name: {
                required: true
            },
            category: {
                required: true
            },
            difficulty: {
                required: true
            },
            muscle_group: {
                required: true
            },
            instructions: {
                required: true
            },
            safety_notes: {
                required: true
            },
            status: {
                required: true
            }
        },
        messages: {
            name: {
                required: "Exercise name is required"
            },
            category: {
                required: "Category is required"
            },
            difficulty: {
                required: "Difficulty is required"
            },
            muscle_group: {
                required: "Muscle group is required"
            },
            instructions: {
                required: "Instructions are required"
            },
            safety_notes: {
                required: "Safety notes are required"
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