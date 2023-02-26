//Feedback Form
let  feedback = {
    submit: function($form) {
        let formURL = $form.attr('action');
        let data = new FormData();
        let form_array = $form.serializeArray();
        for (let i = 0; i < form_array.length; i++) {
            data.append(form_array[i].name, form_array[i].value);
        }
        // Check file form
        if ($form.find('input[type=file]').is('[data-accept-imgfile]')) {
            let file = $form.find('input[type=file]')[0].files[0]
            if(file){
                if(file.size > 5242880 || !["image/jpeg", "image/png", "application/pdf"].includes(file.type)){
                    $form.find("input[type=file]").addClass("error");
                    return false
                } else {
                    data.append('file', file);
                }
            }
        }
        $.ajax({
            url: formURL,
            data:  data,
            processData: false,
            contentType: false,
            method: 'POST',
            success: function(data) {
                $form.replaceWith(data).show();
            },
        });
        return false;
    }
};

//Ajax Send
$(document).on('submit', '.feedback-form', function(e) {
    e.preventDefault();
    feedback.submit($(this));
});


//Custom Switch
$('body').on('click', '.switch', function(){
    let form_selector = '#'+$(this).parents('form').attr('id');
    $(form_selector+' .switch').removeClass('active');
    $(this).addClass('active');
    if($(this).hasClass('on')){
        $(form_selector+' [name$="flag"]').val('on');
    }
    if($(this).hasClass('fake1')){
        $(form_selector+' [name$="flag"]').val('fake1');
    }
    if($(this).hasClass('fake2')){
        $(form_selector+' [name$="flag"]').val('fake2');
    }
    if($(this).hasClass('fake3')){
        $(form_selector+' [name$="flag"]').val('fake3');
    }
});


//Reload form
function ajaxReset($form) {
    let formURL = $form.data("reset-url");
    let formKey = $form.data('key');
    $.ajax({
        url: formURL,
        data:  { 'form_key' : formKey },
        method: 'GET',
        success: function(data) {
           $form.replaceWith(data).show();
        }
    });
    return false;
};

//Export Function
export default ajaxReset;
