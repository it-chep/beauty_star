$(document).ready(function () {
    const $actionBtn = $('.action_btn_container');

    const workerId = getCookie('worker_id');
    const serviceId = getCookie('service_id');

    function getPeriods(selectedDate) {
        $actionBtn.css('display', 'none')
        $.ajax({
            url: $('.container').data('url'),
            method: 'GET',
            data: {
                'date': selectedDate
            },
            success: function (response) {
                const $schedulesBlock = $('.schedules-block');

                $schedulesBlock.empty();
                if (response.schedule_periods && Array.isArray(response.schedule_periods) && response.schedule_periods.length > 0) {
                    response.schedule_periods.forEach(slot => {
                        const $slotElement = $('<div class="schedule_period"></div>')
                            .addClass('time-slot')
                            .attr('data-id', `schedulePeriodId_${slot.id}`)
                            .text(slot.date_time_start);
                        $slotElement.on('click', function () {
                            $('.time-slot').removeClass('active_period');
                            $(this).addClass('active_period');
                            $actionBtn.css('display', 'block')
                        })
                        $schedulesBlock.append($slotElement);
                    });
                } else {
                    $schedulesBlock.append(
                        $('<div class="empty-periods">В этот день запись невозможна, пожалуйста, выберите другой</div>')
                    );
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    }

    const $datepicker = $('.datepicker');
    const $monthYear = $datepicker.find('.month-year');
    const $daysContainer = $datepicker.find('.days');
    const $prevMonthButton = $datepicker.find('.prev-month');
    const $nextMonthButton = $datepicker.find('.next-month');

    let currentDate = new Date();
    let today = new Date();

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();

        const monthName = date.toLocaleDateString('ru-RU', {month: 'long'});
        const formattedMonthName = monthName.charAt(0).toUpperCase() + monthName.slice(1);
        const displayYear = year === today.getFullYear() ? '' : year;

        $monthYear.text(`${formattedMonthName} ${displayYear}`);

        $daysContainer.empty();

        const firstDayOfMonth = new Date(year, month, 1);
        const lastDayOfMonth = new Date(year, month + 1, 0);
        const firstWeekDay = firstDayOfMonth.getDay() === 0 ? 7 : firstDayOfMonth.getDay();
        const daysInMonth = lastDayOfMonth.getDate();

        for (let i = 1; i < firstWeekDay; i++) {
            const emptySpan = $('<span></span>');
            $daysContainer.append(emptySpan);
        }

        for (let i = 1; i <= daysInMonth; i++) {
            const daySpan = $('<span class="datepicker-day"></span>');
            const innerSpan = $('<span></span>').text(i).attr('data-date', new Date(year, month, i + 1).toISOString().split('T')[0]);

            const dayDate = new Date(year, month, i);
            if (dayDate < today.setHours(0, 0, 0, 0)) {
                daySpan.addClass('disabled');
            }
            if (dayDate.toDateString() === today.toDateString() || (month !== today.getMonth() && i === 1)) {
                daySpan.addClass('active');
                const formattedDate = `${dayDate.getFullYear()}-${(dayDate.getMonth() + 1).toString().padStart(2, '0')}-${dayDate.getDate().toString().padStart(2, '0')}`;
                getPeriods(formattedDate);
            }

            daySpan.append(innerSpan);
            $daysContainer.append(daySpan);
        }
        const prevMonthDate = new Date(year, month - 1, 1);
        if (prevMonthDate < new Date(today.getFullYear(), today.getMonth(), 1)) {
            $prevMonthButton.css("cursor", "not-allowed");
        } else {
            $prevMonthButton.css("cursor", "pointer");
        }
    }

    $prevMonthButton.on('click', function () {
        if ($(this).css('cursor') === 'not-allowed') {
            return
        }
        currentDate.setMonth(currentDate.getMonth() - 1);
        $('.schedules-block').empty()
        renderCalendar(currentDate);
    });

    $nextMonthButton.on('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        $('.schedules-block').empty()
        renderCalendar(currentDate);
    });

    $daysContainer.on('click', 'span:not(.disabled)', function () {
        $daysContainer.find('span').removeClass('active');
        $(this).addClass('active');

        const selectedDate = $(this).find('span').attr('data-date');
        if (!selectedDate) {
            return
        }

        const dayText = $(this).text().trim();
        if (dayText.length === 2) {
            $(this).find('span').addClass('double-digit');
        } else {
            $(this).find('span').removeClass('double-digit');
        }

        getPeriods(selectedDate);
    });

    $actionBtn.on('click', function () {
        const $period = $('.active_period');
        const periodId = $period.data('id').replace('schedulePeriodId_', '');
        let url
        if (workerId === undefined && serviceId === undefined) {
            url = `${$(this).data('url')}?period_id=${periodId}`
        } else if (workerId === undefined && serviceId !== undefined) {
            url = `${$(this).data('url')}?period_id=${periodId}&service_id=${serviceId}`
        } else if (workerId !== undefined && serviceId === undefined) {
            url = `${$(this).data('url')}?worker_id=${workerId}&period_id=${periodId}`
        } else {
            url = `${$(this).data('url')}?worker_id=${workerId}&service_id=${serviceId}&period_id=${periodId}`
        }

        document.cookie = `period_id=${periodId}; path=/`;
        window.location = url
    })

    renderCalendar(currentDate);
});