//Filter Form
function ajax_send($form, pagination=false, page=''){
    //Serialize Form
    let formURL = $form.attr("action") + page;
    let form_array = $form.serializeArray();
    let data = {};
    for (let i = 0; i < form_array.length; i++)
        data[form_array[i].name] = form_array[i].value;

    //Load Content
    $.get(formURL, data, function(data){
        if (pagination) {
            //Update pagination
            $('.show-more').replaceWith(data['html']);
            $('.loader-js').removeClass('active');
        }
        else {
            //Load Catalog Card
            $('.product_list_ajax').html(data['html']);
            //Add Count Card
            $('.products_count span').html(data['products_count']);
        }

        showMoreFilter();
    });
}

//Filter submit ajax
$('.filter-form').on('submit', function(e) {
    e.preventDefault();
    $('.filter__btn--mobile').addClass('active');
    $('.filter__option').removeClass('open');
    ajax_send($(this));
});

//Filter submit ajax with change select
$('.filter-form').on('change', '#id_dir', function(e) {
    e.preventDefault();
    $('.filter__option').removeClass('open');
    ajax_send($('.filter-form'));
})

//Filter reset ajax
$(document).on('click', '.filter-reset-js', function(e) {
    e.preventDefault();
    $('.filter-form').each(function(index, form) {
        form.reset();
    });
    $('.filter__option-input--min').val($('.filter__option-input--min').attr('min'));
    $('.filter__option-input--max').val($('.filter__option-input--min').attr('max'));
    $('.filter__option').removeClass('open');
    $('.filter__btn--mobile').removeClass('active');
    ajax_send($('.filter-form'));
});

//Filter With Show More
function showMoreFilter() {
    $('.show-more').on('click', 'a', function(e) {
        e.preventDefault();
        $('.loader-js').addClass('active');
        let form = $('.filter-form');
        ajax_send(form, pagination=true, page=$(this).attr('href'));
    });
}
showMoreFilter();

function showMoreNovelties() {
    $('.show-more-novelties').on('click', 'a.show-more-novelties__btn', function(e) {
        e.preventDefault();
        $('.loader-js').addClass('active');
        //Load Root Novelties
        $.get($(this).data('url')+$(this).attr('href'), function(data){
            $('.show-more-novelties').replaceWith(data['html']);
            $('.loader-js').removeClass('active');
            showMoreNovelties();
        });
    })
}
showMoreNovelties();

function showMorePages() {
    $('.show-more-pages').on('click', 'a.show-more-pages__btn', function(e) {
        e.preventDefault();
        $('.loader-js').addClass('active');
        //Load Page Children
        $.get($('.show-more-pages').data('url')+$(this).attr('href'), function(data){
            $('.show-more-pages').replaceWith(data['html']);
            $('.loader-js').removeClass('active');
            showMorePages();
        });
    })
}
showMorePages();
