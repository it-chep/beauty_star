$(document).ready(function () {
    function getWorkerIdFromURL() {
        const url = window.location.href;
        const parts = url.split('/');
        return parts[parts.length - 2];
    }

    const workerId = getWorkerIdFromURL();
    const serviceId = getCookie('service_id');
    const periodId = getCookie('period_id');
    const $actionBtnContainer = $('.action_btn_container')
    let url

    if (periodId === undefined && serviceId === undefined) {
        url = `${$actionBtnContainer.data('url')}?worker_id=${workerId}`
    } else if (periodId === undefined && serviceId !== undefined) {
        url = `${$actionBtnContainer.data('url')}?worker_id=${workerId}&service_id=${serviceId}`
    } else if (periodId !== undefined && serviceId === undefined) {
        url = `${$actionBtnContainer.data('url')}?worker_id=${workerId}&period_id=${periodId}`
    } else {
        url = `${$actionBtnContainer.data('url')}?worker_id=${workerId}&service_id=${serviceId}&period_id=${periodId}`
    }

    $actionBtnContainer.on('click', function () {
        document.cookie = `worker_id=${workerId}; path=/`;
        window.location = url
    });
});