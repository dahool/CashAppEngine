$(function(){
    $(document).on("pageshow", function(event, ui) {
		createSwipeMenu();
    });
    $('body').on('tap', function(e){
        // if the triggering object is a button, fire it's tap event
        if (e.target.className.indexOf('aSwipeBtn') >= 0) {
            $(e.target).trigger('click');
        }
        // remove any existing buttons
        $('.divSwipe').remove();
    });
})

function createSwipeMenu() {
    $("li[swipe-options]:visible").each(function() {
		$('.divSwipe').remove();
        var $li = $(this);
        var options = $li.attr("swipe-options");
        var opts = $.parseJSON(options);
		// add swipe event to the list item, removing it first (if it exists)
        var direction = 'swipe'+opts.direction;
        var fn = function(e){
            $('.divSwipe').remove();
            e.stopPropagation();
            e.preventDefault();              
			// create buttons and div container
			var $divSwipe = $('<div class="divSwipe"></div>');
			$li.prepend($divSwipe);
			$.each(opts.buttons, function(index, obj) {
				var $b = $('<a>'+obj.value+'</a>').attr({
					'class': 'aSwipeBtn ui-btn-up-'+obj.style,
					'href': obj.href
				});
				$divSwipe.prepend($b);	
			});
			// insert buttons into divSwipe
			$divSwipe.height($li.innerHeight());
			$divSwipe.show(100);
			// add escape route for swipe menu
		};
        $li.off(direction, fn).on(direction, fn);
    });
}
