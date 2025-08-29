document.addEventListener('DOMContentLoaded', () => {
            let currentMonth = new Date().getMonth();
            let currentYear = new Date().getFullYear();
            let allEvents = [];

            const currentMonthYearEl = document.getElementById('current-month-year');
            const calendarBody = document.getElementById('calendar-body');
            const prevMonthBtn = document.getElementById('prev-month');
            const nextMonthBtn = document.getElementById('next-month');

            /**
             * Función para obtener los eventos del backend.
             * Utiliza la ruta URL de Django que apunta a tu vista 'lista_eventos_api'.
             */
            const fetchEventsFromAPI = async () => {
                const url = '/eventos/api/eventos/';
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error('No se pudo obtener la lista de eventos.');
                    }
                    const data = await response.json();
                    return data.map(event => ({
                        ...event,
                        fecha: new Date(event.fecha)
                    }));
                } catch (error) {
                    console.error('Error al obtener los eventos:', error);
                    return [];
                }
            };

            const renderCalendar = () => {
                calendarBody.innerHTML = '';
                const today = new Date();
                const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
                const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);

                let firstDayOfWeek = (firstDayOfMonth.getDay() + 6) % 7;
                const totalDays = lastDayOfMonth.getDate();

                const monthName = new Intl.DateTimeFormat('es-ES', { month: 'long' }).format(firstDayOfMonth);
                currentMonthYearEl.textContent = `${monthName} ${currentYear}`;

                for (let i = 0; i < firstDayOfWeek; i++) {
                    const emptyDay = document.createElement('div');
                    emptyDay.classList.add('calendar-day', 'empty');
                    calendarBody.appendChild(emptyDay);
                }

                for (let day = 1; day <= totalDays; day++) {
                    const dayEl = document.createElement('div');
                    dayEl.classList.add('calendar-day');

                    const date = new Date(currentYear, currentMonth, day);

                    if (date.getFullYear() === today.getFullYear() && date.getMonth() === today.getMonth() && date.getDate() === today.getDate()) {
                        dayEl.classList.add('today');
                    }

                    const dayNumberEl = document.createElement('span');
                    dayNumberEl.classList.add('day-number');
                    dayNumberEl.textContent = day;
                    dayEl.appendChild(dayNumberEl);

                    const eventsForThisDay = allEvents.filter(event => {
                        const eventDate = event.fecha;
                        return eventDate.getFullYear() === currentYear && eventDate.getMonth() === currentMonth && eventDate.getDate() === day;
                    });

                    eventsForThisDay.forEach(event => {
                        const eventEl = document.createElement('div');
                        eventEl.classList.add('event');
                        eventEl.textContent = event.titulo;
                        dayEl.appendChild(eventEl);
                    });

                    calendarBody.appendChild(dayEl);
                }
            };

            prevMonthBtn.addEventListener('click', () => {
                currentMonth--;
                if (currentMonth < 0) {
                    currentMonth = 11;
                    currentYear--;
                }
                renderCalendar();
            });

            nextMonthBtn.addEventListener('click', () => {
                currentMonth++;
                if (currentMonth > 11) {
                    currentMonth = 0;
                    currentYear++;
                }
                renderCalendar();
            });

            const init = async () => {
                allEvents = await fetchEventsFromAPI();
                renderCalendar();
            };

            init();
        });