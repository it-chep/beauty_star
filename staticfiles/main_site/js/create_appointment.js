$(document).ready(function () {

    $('#id_notification_choice').select2({
        minimumResultsForSearch: Infinity,
        dropdownParent: $('#id_notification_choice').closest('.form-input__container'),
        width: 'resolve',
    });


    const $checkbox = $('#privacy_policy_checkbox');
    const $hiddenInput = $('#privacy_policy');

    const $form = $('#appointment_form');
    const $actionBtn = $('.action_btn_container');
    $checkbox.on('change', function () {
        if ($checkbox.is(':checked')) {
            $hiddenInput.val('on');
        } else {
            $hiddenInput.val('');
        }
        $(this).closest('.form-input__input_checkbox').find('.form-input__error').remove();
    });

    $form.find('input, textarea, select').on('input change', function () {
        $(this).closest('.form-input').find('.form-input__error').remove();
    });

    $actionBtn.on('click', function () {
        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            data: $form.serialize(),
            success: function (response) {
                if (response.success) {
                    window.location.href = response.redirect_url;
                } else {
                    $('.form-input__error').remove();

                    $.each(response.errors, function (field, errors) {
                        if (field === 'privacy_policy') {
                            $('#privacy_policy').closest('.form-input').append(`<div class="form-input__error">${errors.join(', ')}</div>`);
                        } else {
                            const $field = $(`[name=${field}]`);
                            if ($field.length) {
                                $field.closest('.form-input').append(`<div class="form-input__error">${errors.join(', ')}</div>`);
                            }
                        }
                    });
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

});