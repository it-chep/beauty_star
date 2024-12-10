$(document).ready(function () {
    $('a.smooth-scroll').on('click', function (event) {
        event.preventDefault();
        var target = this.hash;
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 800);

        window.location.hash = target;
    });

    $('body').scroll(function() {
        console.log('Scroll event detected');
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
});