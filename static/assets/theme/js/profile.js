$(document).ready(function () {

    // ✅ PASSWORD FORM VALIDATION
    $("#update-password-form").validate({
        rules: {
            password: {
                required: true,
                minlength: 6
            },
            confirm_password: {
                required: true,
                minlength: 6,
                equalTo: "#password"
            }
        },
        messages: {
            confirm_password: "Confirm password must match new password."
        }
    });

    // ✅ PROFILE FORM VALIDATION
    $("#update-profile-form").validate({
        rules: {
            name: {
                required: true
            },
            brand_color: {
                required: true
            }
        },
        messages: {
            name: {
                required: "Please enter studio name"
            },
            brand_color: {
                required: "Please select brand color"
            }
        }
    });

});