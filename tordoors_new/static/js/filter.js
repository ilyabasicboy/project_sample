//Filter Form
function ajax_send($form, pagination=false, page=''){
    //Serialize Form
    let object = $form.data('object');
    let c_type = $form.data('type');
    let formURL = $form.attr("action") + page;
    let form_array = $form.serializeArray();
    let data = {};
    for (i = 0; i < form_array.length; i++)
        data[form_array[i].name] = form_array[i].value;
        data['object'] = object;
        data['c_type'] = c_type;

    //Load Content
    $.get(formURL, data, function(data){
        if (pagination) {
            //Update pagination
            $('.show-more').replaceWith(data);
            $('.catalog-loader').removeClass('active');
        }
        else {
            //Load Catalog Card
            $('.product_list_ajax').html(data);
            //Check Count Card
            setItemsCount();
        }

        //Check Reset Button
        if ($('.filter-reset-js').hasClass('reset-check-default')) {
            $('.filter-reset-js').removeClass('reset-check-default');
        } else {
            if ($('.filter-reset-js').hasClass('reset-check')) {
                $('.filter-reset-js').removeClass('filter__reset--hidden');
                $('.filter-reset-js').removeClass('reset-check');
                $('.filter-submit-js').parent().addClass('active');
            } else {
                $('.filter-reset-js').addClass('filter__reset--hidden');
                $('.filter-submit-js').parent().removeClass('active');
            }
        }

        //Filter With Show More
        showMoreFilter();
    });
}

//Filter With Select Options
$('.short_filter-form input[name="dir"]').on('change', function() {
    $('.filter-reset-js').addClass('reset-check-default');
    ajax_send($('.short_filter-form'));
});

//Filter With Submit
$('.filter-submit-js').on('click', function(e) {
    e.preventDefault();
    $('.filter-reset-js').addClass('reset-check');
    ajax_send($('.short_filter-form'));
});

//Fast filter submit
$('.fast_filter-submit-js').on('click', function(e) {
    e.preventDefault();
    ajax_send($('#id_filter_form'));
});

//Filter With Reset
$('.filter-reset-js').on('click', function(e) {
    e.preventDefault();
    $('.short_filter-form .filter__inputs').find('input').each(function() {
        let defValue = $(this).prop("defaultValue");
        $(this).val(defValue);
    });
    ajax_send($('.short_filter-form'));
});

//Filter With Show More
function showMoreFilter() {
    $('.show-more').on('click', 'a', function(e) {
        e.preventDefault();
        $('.catalog-loader').addClass('active');
        $('.filter-reset-js').addClass('reset-check-default');
        let form = $('#id_filter_form').hasClass('ajax_filter_form') ? $('#id_filter_form') : $('.short_filter-form');
        ajax_send(form, pagination=true, page=$(this).attr('href'));
    });
}
showMoreFilter();

//Check Count Card
function setItemsCount() {
    $('.filter__counter-number').html($('.hidden_items_count').data('count'));
}

$(document).ready(function() {
    //Check Count Card
    setItemsCount();
});
