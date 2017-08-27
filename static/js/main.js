 $(document).ready(function() {

     if (type) {
         if (type === 'signup' || type === 'complexRegister')
             $("#signup").removeClass('hide').addClass('show');
         if (type === 'login' || type === 'forget_password')
             $("#login").removeClass('hide').addClass('show');
     }

     var signup_action = true;
    $("#signup_bottum").on("click", function (event) {
        event.preventDefault();
        if (signup_action) {
            $("#signup").removeClass('hide').addClass('show');
            $("#login").removeClass('show').addClass('hide');
            login_action = true;
            signup_action = false;
        }
        else {
            $("#signup").removeClass('show').addClass('hide');
            signup_action = true;
        }
    });
     var login_action = true;
    $("#login_bottum").on("click", function (event) {
        event.preventDefault();
        if (login_action) {
            $("#login").removeClass('hide').addClass('show');
            $("#signup").removeClass('show').addClass('hide');
            signup_action = true;
            login_action = false;
        }
        else {
            $("#login").removeClass('show').addClass('hide');
            login_action = true;
        }
    });
});

