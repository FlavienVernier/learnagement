import evenements from './fakedata.js';

document.addEventListener('DOMContentLoaded', () => {
    const calendar = document.getElementById('calendar');
    const calendarHeader = document.getElementById('calendar-header');
    const prevWeekButton = document.getElementById('prev-week');
    const nextWeekButton = document.getElementById('next-week');

    let currentDate = new Date();

    function renderCalendar(date) {
        calendar.innerHTML = '';
        calendarHeader.innerHTML = '';

        // Obtenir le premier jour de la semaine (lundi)
        const startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - date.getDay() + (date.getDay() === 0 ? -6 : 1)); // Si c'est dimanche, reculer de 6 jours

        for (let i = 0; i < 7; i++) {
            const dayDate = new Date(startOfWeek);
            dayDate.setDate(startOfWeek.getDate() + i);

            const isCurrentDay = (new Date().toDateString() === dayDate.toDateString());

            // En-tête du jour avec le nom et le numéro du jour
            const dayHeader = document.createElement('div');
            dayHeader.className = `day-header ${isCurrentDay ? 'current' : ''}`;
            dayHeader.innerHTML = `
                <div class="day-name">${getDayName(i)}</div>
                <div class="date-number">${dayDate.getDate()}</div>
            `;
            calendarHeader.appendChild(dayHeader);

            // Contenu du jour
            const dayElement = document.createElement('div');
            dayElement.className = `day ${isCurrentDay ? 'current' : ''}`;
            dayElement.innerHTML = renderEvents(dayDate);
            calendar.appendChild(dayElement);
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

        return dayEvents.map(event => `
            <div class="event" style="border-left: 5px solid ${event.couleur};">
                ${event.type} (${event.heure} - ${event.duree_h}h)<br>
                ${event.module} - ${event.enseignant} - ${event.salle}
            </div>
        `).join('');
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
