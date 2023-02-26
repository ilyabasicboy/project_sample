$(function () {

    //File Length
    $(document).on('change', '.input-file', function() {
        let file = $(this)[0].files;

        $(this).parent().parent().find('.upload__info').removeClass('error');

        if (file.length == 0 || file.length == '') {
            $(this).next('.upload__btn').children('span').text("Файл не выбран");
            $(this).parent().parent().find('.upload__delete').removeClass('active');
            $(this).parent().parent().find('.upload__info').removeClass('error');
        } else {
            let fileType = '';
            if ($(this).is('[data-accept-img]')) {
                fileType = ['image/jpeg', 'image/png'].includes(file[0].type);
            }
            if ($(this).is('[data-accept-imgfile]')) {
                fileType = ['image/jpeg', 'image/png', 'application/pdf'].includes(file[0].type);
            }

            if (file[0].size < 5242880 && fileType) {
                if (file.length == 1) {
                  var filename = $(this).val().replace(/^.*[\\\/]/, '');
                  $(this).next('.upload__btn').children('span').text(filename);
                }
            } else {
                $(this).parent().parent().find('.upload__info').addClass('error');
                $(this).parent().parent().find('.upload__delete').addClass('active');
                $(this).next('.upload__btn').parent().addClass('hidden');
            }
        }
    });

    //Delete File
    $(document).on('click', '.upload__delete', function() {
        $(this).parent().parent().find(".input-file").val('');
        $(this).parent().parent().find('.upload__btn').children('span').text("Прикрепить файл").parent().parent().removeClass('hidden');
        $(this).parent().parent().find('.upload__delete').removeClass('active');
        $(this).parent().parent().find('.upload__info').removeClass('error');
    });

});