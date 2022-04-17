$(function () {

    $('.menu-more').each(function () {
        let $nav = $(this);
        let $container = $nav.find('.menu-wrapper');
        let $items = $container.find('.header__menu-item');
        let $overflow = $nav.find('.menu-hidden');
        let $overflowVisible = $nav.find('.menu-visible');
        let $moreCta = $nav.find('.menu-hidden-btn');

        let positions = [];
        $items.each(function () {
            let $item = $(this);
            positions.push({
            $el: $item,
            boundry: Math.round($item.offset().left + $item.outerWidth()) });
        });

        let reposition = function () {
            let navWidth = Math.round($container.outerWidth()) - Math.round($moreCta.outerWidth());

            positions.forEach(function (item) {
                if (item.boundry > navWidth + 220) {
                    item.$el.appendTo($overflow);
                } else {
                    item.$el.appendTo($overflowVisible);
                }
            });

            if ($overflow.children().length > 0) {
                $moreCta.removeClass('hidden');
            } else {
                $moreCta.addClass('hidden');
            }
        };


        if ($(window).outerWidth() > '1024') {
            reposition();
        }

        $(window).on('resize', function() {
            if ($(window).outerWidth() > '1024') {
                reposition();
            } else {
                positions.forEach(function (item) {
                    item.$el.appendTo($overflowVisible);
                    $moreCta.addClass('hidden');
                });
            }
        });

    });

});