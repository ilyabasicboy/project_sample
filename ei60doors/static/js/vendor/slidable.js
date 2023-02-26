$(function () {
    var defaults = {
		minimal: 200,
		controls: ['<span>Подробнее</span>', '<span>Скрыть</span>'],
		speed: 500,
		scroll: false,
	};

	var options;

	$.fn.slidable = function(params) {
		var options = $.extend({}, defaults, params);
		var controller_html = '<a class="controller more">' +
			'<span>' + options.controls[0] + '</span>' +
		'</a>';

		function noHeightData(block) {
			return !$(block).data('height');
		}

		function switchController(controller) {
			var text = $(controller).hasClass('more') ? options.controls[1] : options.controls[0];
			setTimeout(function() {
				$(controller).html("<span>" + text + "</span>");
				$(controller).toggleClass('more');
				$(controller).toggleClass('less');

                if (options.scroll) {
	                controller.onclick = function() {
	                    if ( $(this).hasClass('less') ) {
						    var destination = $(this).siblings('.tall').offset().top;
						}
	                }
                }
			}, options.speed);
		}

		function controllerAction() {
			var self = this;
			var block = $(self).siblings('.tall');
			var new_height = $(self).hasClass('more') ? block.data('height') : options.minimal;
			block.animate({
				height: new_height
			}, options.speed, switchController(self));
			$(block).toggleClass('active');
		}

		function handleClick(controller) {
			$(controller).on('click', controllerAction);
		}

		function init(slidable) {
			$(slidable).children('.tall').each(function() {
				var block = this,
					height = block.clientHeight;
				if (noHeightData(block) && height > options.minimal) {
					$(block).after(controller_html);
					var controller = $(slidable).children('.controller');
					handleClick(controller);
					$(block).data('height', height);
					$(block).height(options.minimal);
					$(block).addClass('active');
				}
			});
		}

		this.each(function() {
			init(this);
		});

		return this;
	};
});