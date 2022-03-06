//Feedback Form
let feedback = {
    submit: function($form){
        let formURL = $form.attr("action");
        let data = new FormData();
        let form_array = $form.serializeArray();
        for (let i = 0; i < form_array.length; i++){
            data.append(form_array[i].name, form_array[i].value);
        }
        //Check File in Form
        if ($form.find('input[type=file]').is('[data-accept-img]')) {
            var file = $form.find('input[type=file]' )[0].files[0]
            if(file){
                if(file.size > 5242880 || !["image/jpeg", "image/png"].includes(file.type)){
                    $form.find("input[type=file]").addClass("error");
                    return false
                } else {
                    data.append('image', file);
                }
            }
        }
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
                //Check Form Letter
                if($form.attr("id") == "id_feedback_form_director_mail"){
                    if (data.match(/thanks/)) {
                        successModal();
                        $form.find('input, textarea').each(function(){
                            $(this).val('')
                        });
                    } else {
                        $form.replaceWith(data).show();
                    }
                } else {
                    $form.replaceWith(data).show();
                }
            },

            error: function(textStatus) {
                $form.toggleClass("loading", false);
            },
        });
        return false;
    }
};

//Ajax Send
$(document).on('submit', '.feedback-form', function(e){
    e.preventDefault();
    feedback.submit($(this));
});

//Reload form
function ajaxReset() {
    let form = $('#thank-you');
    if (form) {
        let formURL = form.data("url");
        let formKey = form.data('form_key');
            $.ajax({
                url: formURL,
                data:  { 'form_key' : formKey },
                method: 'GET',
                success: function(data) {
                    form.closest('#thank-you').replaceWith(data).show();
                }
            });
        return false;
    }
};

//Export Function
export default ajaxReset;

//Open/Auto Close Success Modal
function successModal() {
    $.magnificPopup.open({
        items: {
            src: '#thanks-modal',
        },
        type: "inline",
        removalDelay: 500,
        mainClass: 'mfp-move',
        callbacks: {
            open: function () {
                $("body").addClass("noscroll");
                setTimeout(function(){
                    $.magnificPopup.close();
                }, 4000);
            },
            close: function () {
                $("body").removeClass("noscroll");
            },
        },
    });
};