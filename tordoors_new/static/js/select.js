//Select Init
function selectDefaultInit() {
    $(document).on('click', '.dropdown__button--default-js', function(e) {
        e.stopPropagation();
        $(this).next().toggleClass('dropdown__list--visible');
        $(this).toggleClass('dropdown__button--active');
    });

    $(document).on('click', '.dropdown__item--default-js', function(e) {
        e.preventDefault();
        $(this).parent().prev().find('span').text($(this).text());
        $(this).parent().removeClass('dropdown__button--active').focus();
        $(this).parent().find('.dropdown__item--default-js').removeClass('dropdown__item--active');
        $(this).addClass('dropdown__item--active');
        $(this).removeClass('dropdown__list--visible');
        $(this).parent().next().val($(this).data('value'));
    });

    $(document).on('click', function(e) {
        if(!$(e.target).hasClass('dropdown__button--default-js')) {
            $('.dropdown__list--default-js').removeClass('dropdown__list--visible');
            $('.dropdown__button--default-js').removeClass('dropdown__button--active');
        }
    });
}

//Select Catalog Init
function selectCatalogInit() {
    $(document).on('click', '.dropdown__button--catalog-js', function(e) {
        e.stopPropagation();
        $('.dropdown__list--catalog-js').not(this.nextElementSibling).removeClass('dropdown__list--visible');
        $('.dropdown__button--catalog-js').not(this).removeClass('dropdown__button--active');
        $(this).next().toggleClass('dropdown__list--visible');
        $(this).toggleClass('dropdown__button--active');
    });

    $(document).on('click', '.dropdown__item--catalog-js', function(e) {
        e.preventDefault();
        $(this).parent().prev().find('span').text($(this).text());
        $(this).parent().removeClass('dropdown__button--active').focus();
        $(this).parent().find('.dropdown__item--catalog-js').removeClass('dropdown__item--active');
        $(this).addClass('dropdown__item--active');
        $(this).removeClass('dropdown__list--visible');
        $(this).parent().next().val($(this).data('value')).trigger('change');
    });

    $(document).on('click', function(e) {
        if(!$(e.target).hasClass('dropdown__button--catalog-js')) {
            $('.dropdown__list--catalog-js').removeClass('dropdown__list--visible');
            $('.dropdown__button--catalog-js').removeClass('dropdown__button--active');
        }
    });
}


$(function () {
    //Select Init Start
    selectDefaultInit();
    selectCatalogInit()
});