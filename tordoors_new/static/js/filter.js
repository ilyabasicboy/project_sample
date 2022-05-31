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
            $('.show-more').replaceWith(data['html']);
            $('.catalog-loader').removeClass('active');
        }
        else {
            //Load Catalog Card
            $('.product_list_ajax').html(data['html']);
            //Add Count Card
            $('.filter__counter-number').html(data['products_count']);
        }

        //Check Reset Button
        if ($('.filter-reset-js').hasClass('reset-check-default')) {
            $('.filter-reset-js').removeClass('reset-check-default');
        } else {
            if ($('.filter-reset-js').hasClass('reset-check')) {
                $('.filter-reset-js').removeClass('filter__reset--hidden');
                $('.filter-reset-js').removeClass('reset-check');
                $('.filter__submit').addClass('active');
            } else {
                $('.filter-reset-js').addClass('filter__reset--hidden');
                $('.filter__submit').removeClass('active');
            }
        }

        //Check Count Card and hidden reset button
        if (data['products_count'] == 0) {
            $('.filter-reset-js').addClass('filter__reset--hidden-important');
        } else {
            $('.filter-reset-js').removeClass('filter__reset--hidden-important');
        }

        //Filter With Show More
        showMoreFilter();
    });
}

//Default filter submit Select Options
$('.short_filter-form input[name="dir"]').on('change', function() {
    $('.filter-reset-js').addClass('reset-check-default');
    ajax_send($('.short_filter-form'));
});

//Default filter submit
$('.filter-submit-js-default').on('click', function(e) {
    e.preventDefault();
    $('.filter-reset-js').addClass('reset-check');
    ajax_send($('.short_filter-form'));
});

//Fast filter submit
$('.filter-submit-js-fast').on('click', function(e) {
    e.preventDefault();
    $('.filter-reset-js').addClass('reset-check');
    ajax_send($('#id_filter_form'));
});

//Default filter reset
$(document).on('click', '.filter-reset-js-default', function(e) {
    e.preventDefault();
    $('.short_filter-form .filter__inputs').find('input').each(function() {
        let defValue = $(this).prop('defaultValue');
        $(this).val(defValue);
    });
    ajax_send($('.short_filter-form'));
});

//Fast filter reset
$(document).on('click', '.filter-reset-js-fast', function(e) {
    e.preventDefault();

    const inputMin = $('#id_filter_form').find('#min_price');
    const inputMax = $('#id_filter_form').find('#max_price');
    let defValueMin = inputMin.attr('min');
    let defValueMax = inputMax.attr('max');
    inputMin.val(defValueMin);
    inputMax.val(defValueMax);

    $('#id_filter_form .input:not(.selection__price-input)').find('input').each(function() {
        $(this).val('');
    });
    $('#id_filter_form .dropdown').each(function(index, item) {
        let defValue = $(item).find('.dropdown__item').first().data('value');
        $(item).find('input').val(defValue);

        let initalText = $(item).find('.dropdown__item').first().data('text');
        $(item).find('.dropdown__button span').text(initalText);

        $(item).find('.dropdown__item').removeClass('dropdown__item--active').first().addClass('dropdown__item--active');
    });
    ajax_send($('#id_filter_form'));
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

//Add Count Card
$('.filter__counter-number').html($('.hidden_items_count').data('count'));
