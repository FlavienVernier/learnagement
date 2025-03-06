import evenements from './fakedata.js';

document.addEventListener('DOMContentLoaded', () => {
    const calendarWrapper = document.getElementById('calendar-wrapper');
    const prevWeekButton = document.getElementById('prev-week');
    const nextWeekButton = document.getElementById('next-week');
    const currentMonthElement = document.getElementById('current-month');

    let currentDate = new Date();

    function renderCalendar(date) {
        calendarWrapper.innerHTML = '';
    
        const timeScale = document.createElement('div');
        timeScale.id = 'time-scale';
    
        // Ajouter l'en-tête de l'échelle de temps
        const timeScaleHeader = document.createElement('div');
        timeScaleHeader.id = 'time-scale-header';
        timeScaleHeader.textContent = 'Heures';
        timeScale.appendChild(timeScaleHeader);
    
        for (let hour = 0; hour < 24; hour++) {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = `${String(hour).padStart(2, '0')}:00`;
            timeScale.appendChild(timeSlot);
        }
        calendarWrapper.appendChild(timeScale);
    
        const startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - (date.getDay() === 0 ? 6 : date.getDay() - 1));
    
        updateCurrentMonth(startOfWeek);

    
        for (let i = 0; i < 7; i++) {
            const dayDate = new Date(startOfWeek);
            dayDate.setDate(startOfWeek.getDate() + i);
    
            const isCurrentDay = (dayDate.toDateString() === new Date().toDateString());
    
            const dayColumn = document.createElement('div');
            dayColumn.className = `day-column ${isCurrentDay ? 'current' : ''}`;
            dayColumn.id = getDayName(i).toLowerCase();
    
            const dayHeader = document.createElement('div');
            dayHeader.className = `day-header ${isCurrentDay ? 'current' : ''}`;
            dayHeader.innerHTML = `
                <div class="day-name">${getDayName(i)}</div>
                <div class="date-number">${dayDate.getDate()}</div>
            `;
            dayColumn.appendChild(dayHeader);
    
            const dayContent = document.createElement('div');
            dayContent.className = 'day-content';
    
            // Ajouter les lignes horaires
            for (let hour = 0; hour < 24; hour++) {
                const hourLine = document.createElement('div');
                hourLine.className = 'hour-line';
                hourLine.style.top = `${(hour / 24) * 100}%`;
                dayContent.appendChild(hourLine);
            }
    
            dayContent.innerHTML += renderEvents(dayDate);
            dayColumn.appendChild(dayContent);
    
            calendarWrapper.appendChild(dayColumn);
        }
    }
    

    function getDayName(index) {
        const days = ['LUN.', 'MAR.', 'MER.', 'JEU.', 'VEN.', 'SAM.', 'DIM.'];
        return days[index];
    }

    function renderEvents(date) {
        const dayEvents = evenements.filter(event => {
            const eventDate = new Date(event.date.split('-').reverse().join('-'));
            return eventDate.toDateString() === date.toDateString();
        });

        return dayEvents.map(event => {
            const startHour = parseInt(event.heure.split(':')[0]);
            const startMinute = parseInt(event.heure.split(':')[1]);
            const durationInMinutes = event.duree_h * 60;
            const topPosition = (startHour * 60 + startMinute) / (24 * 60) * 100;
            const eventHeight = durationInMinutes / (24 * 60) * 100;

            return `
                <div class="event" style="top: ${topPosition}%; height: ${eventHeight}%; border-left: 5px solid ${event.couleur};">
                    ${event.module} - ${event.type}<br>
                    (${event.salle})
                </div>
            `;
        }).join('');
    }

    function updateCurrentMonth(date) {
        const dateCopy = new Date(date);
        const monthNames = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
        const startMonth = monthNames[dateCopy.getMonth()];
        const endMonth = monthNames[new Date(dateCopy.setDate(dateCopy.getDate() + 6)).getMonth()];

        currentMonthElement.textContent = (startMonth === endMonth) ? startMonth : `${startMonth} - ${endMonth}`;
    }

    prevWeekButton.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() - 7);
        renderCalendar(currentDate);
    });

    nextWeekButton.addEventListener('click', () => {
        currentDate.setDate(currentDate.getDate() + 7);
        renderCalendar(currentDate);
    });

    renderCalendar(currentDate);
});
