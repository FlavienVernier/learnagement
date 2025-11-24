// ----------------------------------------------------------
// CONFIG
// ----------------------------------------------------------
const API_URL = "http://127.0.0.1:5000";

// Start week at Monday
let currentWeekStart = getMonday(new Date());

// Color palette for events
const EVENT_COLORS = [
    '#4CAF50', '#2196F3', '#FF9800', '#9C27B0', 
    '#F44336', '#00BCD4', '#E91E63', '#3F51B5'
];

// ----------------------------------------------------------
// INIT
// ----------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    renderTimeScale();
    renderWeekColumns(currentWeekStart);
    loadEventsForWeek(currentWeekStart);

    document.getElementById("prev-week").addEventListener("click", () => {
        currentWeekStart.setDate(currentWeekStart.getDate() - 7);
        renderWeekColumns(currentWeekStart);
        loadEventsForWeek(currentWeekStart);
    });

    document.getElementById("next-week").addEventListener("click", () => {
        currentWeekStart.setDate(currentWeekStart.getDate() + 7);
        renderWeekColumns(currentWeekStart);
        loadEventsForWeek(currentWeekStart);
    });
});

// ----------------------------------------------------------
// FETCH EVENTS FROM FLASK
// ----------------------------------------------------------
async function loadEventsForWeek(monday) {
    const start = formatDate(monday);
    const end = formatDate(addDays(monday, 7));

    const url = `${API_URL}/events.json?start=${start}&end=${end}`;

    console.log(`Fetching events from: ${url}`);

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Flask API error: ${response.status}`);

        const events = await response.json();
        console.log(`Loaded ${events.length} events:`, events);
        
        clearEvents();
        placeEvents(events);

    } catch (err) {
        console.error("Failed to fetch from Flask API:", err);
        // Show error message in UI
        showError("Impossible de charger les événements. Vérifiez que le serveur Flask est actif.");
    }
}

// ----------------------------------------------------------
// RENDER TIME SCALE (06:00 → 22:00)
// ----------------------------------------------------------
function renderTimeScale() {
    const timeScale = document.getElementById("time-scale");
    timeScale.innerHTML = "";

    for (let hour = 6; hour <= 22; hour++) {
        const slot = document.createElement("div");
        slot.className = "time-slot";
        slot.textContent = hour.toString().padStart(2, "0") + ":00";
        timeScale.appendChild(slot);
    }
}

// ----------------------------------------------------------
// RENDER WEEK COLUMNS
// ----------------------------------------------------------
function renderWeekColumns(monday) {
    const wrapper = document.getElementById("calendar-wrapper");

    // Remove previous columns but keep time-scale
    wrapper.querySelectorAll(".day-column").forEach(e => e.remove());

    const days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];

    for (let i = 0; i < 7; i++) {
        const date = addDays(monday, i);
        const dayCol = document.createElement("div");
        dayCol.className = "day-column";
        dayCol.dataset.day = formatDate(date);

        const header = document.createElement("div");
        header.className = "day-header";
        
        // Highlight today
        const today = new Date();
        if (formatDate(date) === formatDate(today)) {
            header.classList.add("today");
        }
        
        header.textContent = `${days[i]} ${date.getDate()}/${date.getMonth() + 1}`;

        const content = document.createElement("div");
        content.className = "day-content";

        dayCol.appendChild(header);
        dayCol.appendChild(content);
        wrapper.appendChild(dayCol);
    }

    document.getElementById("current-month").textContent =
        `${monday.toLocaleString("fr-FR", { month: "long" })} ${monday.getFullYear()}`;
}

// ----------------------------------------------------------
// PLACE EVENTS IN THE CALENDAR
// ----------------------------------------------------------
function placeEvents(events) {
    if (!events || events.length === 0) {
        console.log("No events to display");
        return;
    }

    events.forEach((ev, index) => {
        try {
            const start = new Date(ev.start);
            const end = new Date(ev.end);

            // Validate dates
            if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                console.warn("Invalid date for event:", ev);
                return;
            }

            const dayString = formatDate(start);
            const column = document.querySelector(`.day-column[data-day="${dayString}"] .day-content`);
            
            if (!column) {
                console.log(`No column found for date: ${dayString}`);
                return;
            }

            const div = document.createElement("div");
            div.className = "event-block";
            div.textContent = ev.title || "Sans titre";

            // Use backgroundColor from event data, or fallback to color palette
            const eventColor = ev.backgroundColor || EVENT_COLORS[hashString(ev.title || "") % EVENT_COLORS.length];
            div.style.backgroundColor = eventColor;
            div.style.borderLeft = `4px solid ${darkenColor(eventColor)}`;

            // Position inside the column (adjusted for 6 AM start)
            const startHour = start.getHours() + start.getMinutes() / 60;
            const endHour = end.getHours() + end.getMinutes() / 60;
            const duration = endHour - startHour;

            // Adjust position relative to 6 AM (0 position = 6 AM)
            const adjustedStart = startHour - 6;
            
            div.style.top = `${adjustedStart * 60}px`; // 60px per hour, starting from 6 AM
            div.style.height = `${Math.max(duration * 60, 20)}px`; // Minimum 20px height

            // Add time to event text if event is short
            if (duration < 1) {
                div.innerHTML = `<strong>${start.getHours().toString().padStart(2, '0')}:${start.getMinutes().toString().padStart(2, '0')}</strong> ${ev.title || "Sans titre"}`;
            }

            // Tooltip on hover
            div.addEventListener("mouseenter", (e) => showTooltip(ev, div, e));
            div.addEventListener("mouseleave", hideTooltip);

            // Click to go to event detail (if you have event IDs)
            if (ev.id) {
                div.style.cursor = "pointer";
                div.addEventListener("click", () => {
                    window.location.href = `/event/${ev.id}`;
                });
            }

            column.appendChild(div);

        } catch (err) {
            console.error("Error placing event:", ev, err);
        }
    });
}

// ----------------------------------------------------------
// EVENT CLEANUP
// ----------------------------------------------------------
function clearEvents() {
    document.querySelectorAll(".event-block").forEach(e => e.remove());
}

// ----------------------------------------------------------
// TOOLTIP
// ----------------------------------------------------------
function showTooltip(ev, target, mouseEvent) {
    const tooltip = document.getElementById("tooltip");
    tooltip.style.display = "block";
    
    const start = new Date(ev.start);
    const end = new Date(ev.end);
    
    const formatTime = (date) => {
        return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    };

    tooltip.innerHTML = `
        <strong>${ev.title || "Sans titre"}</strong><br>
        📅 ${formatDate(start)}<br>
        🕐 ${formatTime(start)} - ${formatTime(end)}<br>
        ${ev.location ? `📍 ${ev.location}<br>` : ''}
        ${ev.description ? `<br>${ev.description.substring(0, 100)}${ev.description.length > 100 ? '...' : ''}` : ''}
    `;

    // Position tooltip near mouse cursor
    const rect = target.getBoundingClientRect();
    tooltip.style.top = (mouseEvent.clientY - 10) + "px";
    tooltip.style.left = (rect.right + 10) + "px";

    // Check if tooltip goes off screen
    setTimeout(() => {
        const tooltipRect = tooltip.getBoundingClientRect();
        if (tooltipRect.right > window.innerWidth) {
            tooltip.style.left = (rect.left - tooltipRect.width - 10) + "px";
        }
        if (tooltipRect.bottom > window.innerHeight) {
            tooltip.style.top = (window.innerHeight - tooltipRect.height - 10) + "px";
        }
    }, 0);
}

function hideTooltip() {
    document.getElementById("tooltip").style.display = "none";
}

// ----------------------------------------------------------
// ERROR DISPLAY
// ----------------------------------------------------------
function showError(message) {
    const wrapper = document.getElementById("calendar-wrapper");
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #f44336;
        color: white;
        padding: 20px;
        border-radius: 8px;
        font-size: 16px;
        z-index: 1000;
    `;
    wrapper.appendChild(errorDiv);
}

// ----------------------------------------------------------
// UTILITY FUNCTIONS
// ----------------------------------------------------------

// Hash string to get consistent color for same event titles
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return Math.abs(hash);
}

// Darken color for border
function darkenColor(color) {
    const hex = color.replace('#', '');
    const r = Math.max(0, parseInt(hex.substr(0, 2), 16) - 40);
    const g = Math.max(0, parseInt(hex.substr(2, 2), 16) - 40);
    const b = Math.max(0, parseInt(hex.substr(4, 2), 16) - 40);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

function getMonday(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = (day === 0 ? -6 : 1) - day; // Monday = 1
    d.setDate(d.getDate() + diff);
    d.setHours(0, 0, 0, 0); // Reset time
    return d;
}

function formatDate(date) {
    return date.toISOString().split("T")[0];
}

function addDays(date, days) {
    const d = new Date(date);
    d.setDate(d.getDate() + days);
    return d;
}