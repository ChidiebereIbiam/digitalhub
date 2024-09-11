"use strict";

(function ($) {
    "use strict";

    $(window).scroll(function () {
        var window_top = $(window).scrollTop() + 1;

        if (window_top > 50) {
            $('.scroll-to-top').addClass('reveal');
        } else {
            $('.scroll-to-top').removeClass('reveal');
        }
    });




    /*
     * ----------------------------------------------------------------------------------------
     *  SMOTH SCROOL JS
     * ----------------------------------------------------------------------------------------
     */

    $('a.js-scroll-trigger').on('click', function (e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top - 100
        }, 1000);
        e.preventDefault();
    });



})(jQuery);