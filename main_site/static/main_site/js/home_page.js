$(document).ready(function () {
    $('a.smooth-scroll').on('click', function (event) {
        event.preventDefault();
        var target = this.hash;
        var $target = $(target);
        var headerHeight = $('.header').outerHeight();

        $target.css('scroll-margin-top', (headerHeight) + 'px');

        $target[0].scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

        setTimeout(function () {
            window.location.hash = target;
        }, 800);
    });

    $('body').scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('#backToTop').addClass('show');
        } else {
            $('#backToTop').removeClass('show');
        }
    });

    $('#backToTop').on('click', function () {
        $('html, body').animate({scrollTop: 0}, 'slow');
        return false;
    });

    $('.service_group_name').on('click', function () {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            let target = $(this).data('target');
            $(target).find('.services-container').css('display', 'none');
            $(target).css('display', 'none');
        } else {
            $('.service_group_name').removeClass('active');
            $('.services').hide();

            $(this).addClass('active');
            let target = $(this).data('target');
            $(target).find('.services-container').css('display', 'flex');
            $(target).css('display', 'flex');
        }
    });

    let $burger = $('#burger');
    let $mobileNavbar = $('#mobile-navbar');
    $burger.on('input', function () {
        $mobileNavbar.toggleClass('show')
    });

    $('.mobile-header-item').on('click', function () {
        $mobileNavbar.toggleClass('show')
        $('#burger').prop('checked', false);
    });
});