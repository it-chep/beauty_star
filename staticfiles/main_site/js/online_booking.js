$(document).ready(function () {
    function deleteCookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    }

    deleteCookie('worker_id');
    deleteCookie('service_id');
    deleteCookie('period_id');
});