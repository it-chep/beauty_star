$(document).ready(function () {
    $(".subgroup-title").on("click", function () {
        $(this).toggleClass("collapsed");
        $(this).siblings(".item-container").slideToggle();
    });

    $(".item-container").css({
        display: 'none',
    });

    $('.item-container').on('click', function () {
        const serviceId = $(this).attr('id');
        const checkbox = $(`#service_${serviceId}`);

        $('input[name="service-select"]').prop('checked', false);
        checkbox.prop('checked', !checkbox.prop('checked'));

        const serviceContainer = $('.action_btn_container');
        if (serviceContainer.css('display') === 'none') {
            serviceContainer.css('display', 'block');
        }

        const activeCheckboxes = $('input[name="service-select"]:checked').length;
        if (activeCheckboxes === 0) {
            serviceContainer.css('display', 'none');
        }
    });

    $('.action_btn_container').on('click', function () {
        const activeServiceSelect = $('input[name="service-select"]:checked');
        const serviceId = activeServiceSelect.attr('id').replace('service_', '');

        document.cookie = `service_id=${serviceId}; path=/`;

        const workerId = getCookie('worker_id');
        const periodId = getCookie('period_id');
        let url
        if (periodId === undefined && workerId === undefined) {
            url = `${$(this).data('url')}?service_id=${serviceId}`
        } else if (periodId === undefined && workerId !== undefined) {
            url = `${$(this).data('url')}?worker_id=${workerId}&service_id=${serviceId}`
        } else if (periodId !== undefined && workerId === undefined) {
            url = `${$(this).data('url')}?service_id=${serviceId}&period_id=${periodId}`
        } else {
            url = `${$(this).data('url')}?worker_id=${workerId}&service_id=${serviceId}&period_id=${periodId}`
        }

        window.location = url;
    });
});