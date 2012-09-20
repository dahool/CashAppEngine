/*
Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
(function($, undefined ) {
$.widget( "mobile.datebox", $.mobile.widget, {
    options: {
        theme: 'jqm',
        lang: 'en',
        mode: 'scroller',
        disableManualInput: false,
        preset: 'date'
    },
    _create: function(){
        var self = this;
        var o = $.extend(this.options, this.element.data('options'));
        var input = this.element;
/*        var thisTheme = input.parentsUntil(':jqmData(theme)').parent().jqmData('theme');
        var fEl = input.wrap('<div class="ui-input-datebox ui-shadow-inset ui-corner-all ui-body-'+ thisTheme +'"></div>').parent();
        var button = $('<span class="ui-input-clear">&nbsp;</span>').appendTo(fEl).buttonMarkup({icon: 'grid', iconpos: 'notext', corners:true, shadow:true}).css({'vertical-align': 'middle', 'display': 'inline-block'});
  */      
        $(input).scroller(o);
        $(input).on('click', function() {
            $(this).scroller('show');
        });
        
        if (o.disableManualInput) $(input).attr("readonly", true);
    },
});
$(document).bind(
        "pagebeforecreate",
        function(c) {
            $(":jqmData(role='datebox')", c.target).each(
                    function() {
                        $(this).replaceWith(
                                $("<div>").html($(this).clone()).html()
                                        .replace(/\s+type=["']date['"]?/,
                                                ' type="text" '))
                    })
        });
$(document).bind("pagecreate create", function(c) {
    $(document).trigger("dateboxbeforecreate");
    $(":jqmData(role='datebox')", c.target).each(function() {
        if (typeof ($(this).data("datebox")) === "undefined") {
            $(this).datebox();
        }
    })
})
})( jQuery );

