$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const serviceId = urlParams.get('service_id');

    if (serviceId) {
        document.cookie = `service_id=${serviceId}; path=/;`;
    }

    $('.menu-item-container').on('click', function () {
        const workerId = $(this).attr('id');
        $(`#radio_${workerId}`).prop('checked', true);

        const serviceContainer = $('.action_btn_container');
        if (serviceContainer.css('display') === 'none') {
            serviceContainer.css('display', 'block');
        }
    });

    $('.action_btn_container').on('click', function () {
        const activeRadio = $('input[name="radio-group"]:checked');
        if (activeRadio.length > 0) {
            const workerId = activeRadio.attr('id').replace('radio_', '');
            const serviceId = getCookie('service_id');
            const periodId = getCookie('period_id');

            let url
            if (periodId === undefined && serviceId === undefined) {
                url = `${$(this).data('url')}?worker_id=${workerId}`
            } else if (periodId === undefined && serviceId !== undefined) {
                url = `${$(this).data('url')}?worker_id=${workerId}&service_id=${serviceId}`
            } else if (periodId !== undefined && serviceId === undefined) {
                url = `${$(this).data('url')}?worker_id=${workerId}&period_id=${periodId}`
            } else {
                url = `${$(this).data('url')}?worker_id=${workerId}&service_id=${serviceId}&period_id=${periodId}`
            }

            document.cookie = `worker_id=${workerId}; path=/`;
            window.location = url
        } else {
            console.log('No active radio button found.');
        }
    });
});