$(document).ready(function(){

    $("#register_form").validate({

        rules: {

            email: {
                required: true,
                email: true
            },

            password: {
                required: true,
                minlength: 6
            },

            confirm_password: {
                required: true,
                equalTo: "input[name='password']"
            },

            terms: {
                required: true
            }

        },

        messages: {

            email: {
                required: "Please enter email address",
                email: "Please enter valid email"
            },

            password: {
                required: "Please enter password",
                minlength: "Password must be at least 6 characters"
            },

            confirm_password: {
                required: "Please confirm password",
                equalTo: "Password and confirm password must match"
            },

            terms: {
                required: "Please accept Terms & Conditions"
            }

        },

        submitHandler: function(form){
            form.submit();
        }

    });

});