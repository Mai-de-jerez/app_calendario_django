document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                locale: 'es',
                height: 'parent',
                headerToolbar: {
                    left: 'prev,next',
                    center: 'title',
                    right: 'today dayGridMonth,timeGridWeek,timeGridDay'
                },
                events: '/eventos/api/eventos/',
                displayEventTime: false,
                fixedWeekCount: true,
                dayMaxEvents: true // Activa el botón "+X más"
            });
            calendar.render();
        });