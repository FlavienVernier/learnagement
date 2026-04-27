/**
 * ----------------------------------------------------------
 * CONFIGURATION & BASE URL
 * ----------------------------------------------------------
 */

const PYTHON_BACKEND_URL = `http://${window.location.hostname}` // window.ENV.BACKEND_URL;
const PYTHON_BACKEND_PORT = window.ENV.BACKEND_PORT || "8000";

const getPythonBackendUrl = (endpoint) => {
    return `${PYTHON_BACKEND_URL}:${PYTHON_BACKEND_PORT}/${endpoint}`;
};

/**
 * ----------------------------------------------------------
 * CORE API FUNCTION (Equivalent de python_endpoint)
 * ----------------------------------------------------------
 */

async function pythonEndpoint(method, url, data = null, token) {
    console.log(`API Request: ${method} ${url} with data:`, data);
    console.log(`Using token: ${token}`);
    const headers = {
        "Authorization": `Bearer ${token}`
    };

    let finalUrl = url;
    const options = {
        method: method,
        headers: headers
    };

    console.log(options);

    // Configuration des headers et du corps selon la méthode
    if (method === "GET" || method === "DELETE") {
        headers["Content-Type"] = "application/x-www-form-urlencoded";
        
        // Conversion du data en Query String pour le GET
        if (method === "GET" && data) {
            const queryString = new URLSearchParams(data).toString();
            finalUrl += (finalUrl.includes('?') ? '&' : '?') + queryString;
        }
    } else {
        headers["Content-Type"] = "application/json";
        if (data) {
            options.body = JSON.stringify(data);
        }
    }

    try {
        const response = await fetch(finalUrl, options);
        console.log("Appel API vers :", finalUrl);


        // Gestion des erreurs HTTP (équivalent status check en PHP)
        if (response.status === 401) throw new Error("Invalid or expired token");
        if (response.status === 403) throw new Error("Access denied - missing required role");
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

        // Lecture de la réponse
        const text = await response.text();
        
        // Gestion du cas "[]" ou réponse vide
        if (!text || text === "[]") return [];

        try {
            return JSON.parse(text);
        } catch (e) {
            console.error("JSON parsing error:", text);
            return [];
        }

    } catch (error) {
        console.error("Connection error:", error.message);
        throw error; 
    }
}

/**
 * ----------------------------------------------------------
 * WRAPPERS METHODES HTTP
 * ----------------------------------------------------------
 */

export const getEndpoint = (url, token, data = null) => pythonEndpoint("GET", url, data, token);
export const postEndpoint = (url, data, token) => pythonEndpoint("POST", url, data, token);
export const patchEndpoint = (url, data, token) => pythonEndpoint("PATCH", url, data, token);
export const deleteEndpoint = (url, token) => pythonEndpoint("DELETE", url, null, token);

/**
 * ----------------------------------------------------------
 * FONCTIONS RESSOURCES SPECIFIQUES
 * ----------------------------------------------------------
 */

export const getEnseignants = (token) => {
    const url = getPythonBackendUrl("enseignants/");
    return getEndpoint(url, token);
};

export const getEtudiants = (token) => {
    const url = getPythonBackendUrl("etudiants/");
    return getEndpoint(url, token);
};

export const getFilieres = (token) => {
    const url = getPythonBackendUrl("filieres/");
    return getEndpoint(url, token);
};

export const getStatuts = (token) => {
    const url = getPythonBackendUrl("statuts/");
    return getEndpoint(url, token);
};

export const getPromos = (token) => {
    const url = getPythonBackendUrl("promos/");
    return getEndpoint(url, token);
};

export const getGroupeTypes = (token) => {
    const url = getPythonBackendUrl("groupe_types/");
    return getEndpoint(url, token);
};

export const getSeanceTypes = (token) => {
    const url = getPythonBackendUrl("seance_types/");
    return getEndpoint(url, token);
};

export const getCalendar = (token) => {
    const url = getPythonBackendUrl("user/calendar/");
    return getEndpoint(url, token);
};

export const updateCalendar = (token, data) => {
    const url = getPythonBackendUrl("user/calendar/update/");
    return postEndpoint(url, data, token); 
};