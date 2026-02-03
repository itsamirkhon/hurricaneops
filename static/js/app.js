/**
 * HurricaneOps - Command & Control Platform
 * Powered by Cerebras AI
 */

// ====== CONFIGURATION ======
const API_BASE = '/api';
const REFRESH_INTERVAL = 30000;

// ====== SVG ICONS (Apple SF Symbol style) ======
const ICONS = {
    flood_rescue: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>`,
    medical_emergency: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`,
    structural_collapse: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l7-4 7 4v14"/><path d="M9 21v-6h6v6"/></svg>`,
    evacuation: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>`,
    utility_failure: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`,
    road_blockage: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 14.14 14.14"/></svg>`,
    boat: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.5 0 2.5 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4a12 12 0 0 0 2.81 7.76"/></svg>`,
    helicopter: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M4 6h16M12 6v8"/><path d="M8 14h8l2 4H6l2-4z"/></svg>`,
    ground_vehicle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 17h4V5H2v12h3"/><path d="M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h1"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>`,
    drone: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="6" height="6" rx="1"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="m7 7 2 2M15 7l2-2M7 17l2-2M15 17l2 2"/></svg>`,
    medical_team: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/></svg>`,
    rescue_team: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`,
    people: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    location: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>`,
    alert: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
    situation_analyst: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>`,
    triage_agent: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`,
    resource_coordinator: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>`,
    routing_agent: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>`,
    command_agent: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`,
    send: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2L15 22l-4-9-9-4 20-7z"/></svg>`,
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>`
};

// Apple system colors
const AGENT_COLORS = {
    situation_analyst: '#BF5AF2',  // Purple
    triage_agent: '#FF453A',       // Red
    resource_coordinator: '#30D158', // Green
    routing_agent: '#FF9F0A',      // Orange
    command_agent: '#64D2FF'       // Cyan
};

const AGENT_NAMES = {
    situation_analyst: 'Analyst',
    triage_agent: 'Triage',
    resource_coordinator: 'Resources',
    routing_agent: 'Routing',
    command_agent: 'Command'
};

// ====== STATE ======
let map;
let incidentMarkers = {};
let assetMarkers = {};
let incidents = [];
let assets = [];
let showIncidents = true;
let showAssets = true;
let agentSessionActive = false;
let totalMessages = 0;
let totalComputationMs = 0;
let creatingIncident = false;
let authToken = localStorage.getItem('hurricane_auth_token');
let userRole = localStorage.getItem('hurricane_user_role');

// ====== AUTHENTICATION ======
function checkAuth() {
    // DEMO MODE: Always allow access
    document.getElementById('login-modal').classList.remove('active');
    return true;

    /* Original Auth Check
    if (!authToken) {
        document.getElementById('login-modal').classList.add('active');
        return false;
    }
    document.getElementById('login-modal').classList.remove('active');
    return true;
    */
}

async function login(username, password) {
    const errorEl = document.getElementById('login-error');
    errorEl.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE}/auth/token`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Invalid credentials');

        const data = await response.json();
        authToken = data.access_token;
        userRole = data.role;

        localStorage.setItem('hurricane_auth_token', authToken);
        localStorage.setItem('hurricane_user_role', userRole);

        checkAuth();
        loadData(); // Initial load after login
    } catch (e) {
        errorEl.textContent = e.message;
        errorEl.style.display = 'block';
    }
}

function logout() {
    authToken = null;
    userRole = null;
    localStorage.removeItem('hurricane_auth_token');
    localStorage.removeItem('hurricane_user_role');
    checkAuth();
}

async function authenticatedFetch(url, options = {}) {
    if (!options.headers) options.headers = {};
    // DEMO MODE: Token not strictly required by backend anymore, but we can pass a dummy
    options.headers['Authorization'] = `Bearer demo-token`;

    const response = await fetch(url, options);

    // DEMO MODE: Ignore 401 just in case
    // if (response.status === 401) {
    //     logout();
    //     throw new Error('Unauthorized');
    // }

    return response;
}


// ====== INITIALIZATION ======
document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    initializeEventListeners();
    loadData();
    loadActivityLog();
    startClock();
    checkAIStatus();
    checkAIStatus();
    setupWebSocket();
    // Keep polling as backup, but rely on WS
    setInterval(loadData, REFRESH_INTERVAL);

    // Auth Listeners
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        await login(username, password);
    });

    // Check auth on load
    if (!checkAuth()) return;
});

// ====== WEBSOCKET ======
function setupWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    // Determine active port if testing locally (e.g. ngrok vs localhost)
    // The browser handles host automatically

    console.log(`Connecting to WebSocket: ${wsUrl}`);
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log('WebSocket connected');
        // socket.send('Hello Server!');
    };

    socket.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            if (msg.type === 'update') {
                console.log('Received system update');
                loadData();
            } else if (msg.type === 'action_log') {
                addActivity('system', `[WS] ${msg.message}`);
                loadData();
            }
        } catch (e) {
            console.error('WS Message parsing error:', e);
        }
    };

    socket.onclose = () => {
        console.log('WebSocket disconnected, reconnecting in 5s...');
        setTimeout(setupWebSocket, 5000);
    };

    socket.onerror = (err) => {
        console.error('WebSocket error:', err);
    };
}

// ====== MAP ======
function initializeMap() {
    map = L.map('map', { center: [27.95, -82.46], zoom: 12, zoomControl: false });
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map);
    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    // Map click handler for creating incidents
    map.on('click', (e) => {
        if (creatingIncident) {
            document.getElementById('incident-lat').value = e.latlng.lat;
            document.getElementById('incident-lng').value = e.latlng.lng;
            document.querySelector('.form-hint').textContent = `Location: ${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)}`;
        }
    });
}

function updateMapMarkers() {
    Object.values(incidentMarkers).forEach(m => map.removeLayer(m));
    Object.values(assetMarkers).forEach(m => map.removeLayer(m));
    incidentMarkers = {};
    assetMarkers = {};

    if (showIncidents) {
        incidents.forEach(incident => {
            if (incident.status === 'resolved') return;
            const icon = createIncidentIcon(incident.priority, incident.type);
            const marker = L.marker([incident.location.latitude, incident.location.longitude], { icon }).addTo(map);
            marker.bindPopup(createIncidentPopup(incident));
            incidentMarkers[incident.id] = marker;
        });
    }

    if (showAssets) {
        assets.forEach(asset => {
            const icon = createAssetIcon(asset.type, asset.status);
            const marker = L.marker([asset.location.latitude, asset.location.longitude], { icon }).addTo(map);
            marker.bindPopup(createAssetPopup(asset));
            assetMarkers[asset.id] = marker;
        });
    }
}

function createIncidentIcon(priority, type) {
    const colors = { critical: '#ef4444', high: '#f97316', medium: '#eab308', low: '#22c55e' };
    const svg = ICONS[type] || ICONS.alert;
    return L.divIcon({
        className: 'custom-marker-container',
        html: `<div class="custom-marker" style="background: ${colors[priority]}; border: 2px solid rgba(255,255,255,0.8);">${svg}</div>`,
        iconSize: [40, 40], iconAnchor: [20, 20]
    });
}

function createAssetIcon(type, status) {
    const colors = {
        available: '#22c55e', deployed: '#3b82f6', en_route: '#eab308', on_scene: '#f97316', returning: '#06b6d4'
    };
    const svg = ICONS[type] || ICONS.rescue_team;
    return L.divIcon({
        className: 'custom-marker-container',
        html: `<div class="custom-marker" style="background: ${colors[status] || '#3b82f6'}; border: 2px solid rgba(255,255,255,0.8);">${svg}</div>`,
        iconSize: [40, 40], iconAnchor: [20, 20]
    });
}

function createIncidentPopup(incident) {
    return `<div style="min-width: 200px; font-family: 'Fira Sans', sans-serif;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-family: 'Fira Code'; font-size: 11px; color: #06b6d4;">${incident.id}</span>
            <span style="background: ${getPriorityColor(incident.priority)}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px;">${incident.priority}</span>
        </div>
        <div style="font-weight: 600; margin-bottom: 4px;">${formatIncidentType(incident.type)}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">${incident.description}</div>
        <div style="display: flex; gap: 8px;">
            <button onclick="showDeployModal('${incident.id}')" style="flex:1; padding: 6px; background: #3b82f6; color: white; border: none; border-radius: 4px; cursor: pointer;">Deploy</button>
            <button onclick="resolveIncident('${incident.id}')" style="padding: 6px 12px; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer;">✓</button>
        </div>
    </div>`;
}

function createAssetPopup(asset) {
    return `<div style="min-width: 180px; font-family: 'Fira Sans', sans-serif;">
        <div style="font-weight: 600; margin-bottom: 4px;">${asset.name}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">${formatAssetType(asset.type)}</div>
        <span style="background: ${getStatusColor(asset.status)}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px;">${asset.status}</span>
        ${asset.assigned_incident ? `<div style="margin-top: 8px;"><button onclick="recallAsset('${asset.id}')" style="width: 100%; padding: 6px; background: #f59e0b; color: white; border: none; border-radius: 4px; cursor: pointer;">Recall</button></div>` : ''}
    </div>`;
}

// ====== DATA LOADING ======
async function loadData() {
    if (!authToken) return; // Don't load if not active
    try {
        const [incidentsRes, assetsRes, summaryRes] = await Promise.all([
            authenticatedFetch(`${API_BASE}/incidents`),
            authenticatedFetch(`${API_BASE}/assets`),
            authenticatedFetch(`${API_BASE}/summary`)
        ]);
        incidents = await incidentsRes.json();
        assets = await assetsRes.json();
        const summary = await summaryRes.json();
        updateIncidentsList();
        updateAssetsList();
        updateStats(summary);
        updateWeather(summary.weather);
        updateMapMarkers();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateIncidentsList() {
    const container = document.getElementById('incidents-list');
    document.getElementById('incident-count').textContent = incidents.filter(i => i.status !== 'resolved').length;
    const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    const sorted = [...incidents].filter(i => i.status !== 'resolved').sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

    container.innerHTML = sorted.map(incident => `
        <div class="incident-card ${incident.priority}" data-id="${incident.id}">
            <div class="incident-header">
                <span class="incident-id">${incident.id}</span>
                <span class="incident-priority ${incident.priority}">${incident.priority}</span>
            </div>
            <div class="incident-type">${ICONS[incident.type] || ICONS.alert} ${formatIncidentType(incident.type)}</div>
            <div class="incident-description">${incident.description}</div>
            <div class="incident-meta">
                <span>${ICONS.people} ${incident.affected_count}</span>
            </div>
            <div class="incident-actions">
                <button class="action-btn" onclick="event.stopPropagation(); showDeployModal('${incident.id}')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13"/><path d="M22 2L15 22l-4-9-9-4 20-7z"/></svg>
                    Deploy
                </button>
                <button class="action-btn resolve" onclick="event.stopPropagation(); resolveIncident('${incident.id}')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>
                    Resolve
                </button>
            </div>
        </div>
    `).join('');
}

function updateAssetsList() {
    const container = document.getElementById('assets-list');
    document.getElementById('asset-count').textContent = assets.length;
    container.innerHTML = assets.map(asset => `
        <div class="asset-card" data-id="${asset.id}">
            <div class="asset-icon">${ICONS[asset.type] || ICONS.rescue_team}</div>
            <div class="asset-info">
                <div class="asset-name">${asset.name}</div>
                <div class="asset-location">${asset.assigned_incident || 'Available'}</div>
            </div>
            <span class="asset-status ${asset.status}">${asset.status.replace('_', ' ')}</span>
        </div>
    `).join('');
}

function updateStats(summary) {
    animateValue('stat-critical', summary.critical_incidents);
    animateValue('stat-affected', summary.total_affected);
    animateValue('stat-available', summary.available_assets);
    animateValue('stat-deployed', summary.deployed_assets);
}

function animateValue(elementId, newValue) {
    const el = document.getElementById(elementId);
    const current = parseInt(el.textContent) || 0;
    if (current === newValue) return;
    const diff = newValue - current;
    const steps = 15;
    let step = 0;
    const animate = () => {
        step++;
        el.textContent = Math.round(current + (diff / steps) * step);
        if (step < steps) requestAnimationFrame(animate);
        else el.textContent = newValue;
    };
    requestAnimationFrame(animate);
}

function updateWeather(weather) {
    document.getElementById('hurricane-cat').textContent = weather.hurricane_category || '-';
    document.getElementById('wind-speed').textContent = Math.round(weather.wind_speed_mph) || '-';
    document.getElementById('storm-surge').textContent = weather.storm_surge_feet?.toFixed(1) || '-';
}

// ====== ACTIONS ======
async function deployAsset(assetId, incidentId) {
    showLoading();
    try {
        const response = await authenticatedFetch(`${API_BASE}/actions/deploy`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ asset_id: assetId, incident_id: incidentId })
        });
        const result = await response.json();
        addActivity('deploy', result.result?.message || `Deployed ${assetId} to ${incidentId}`);
        loadData();
        loadActivityLog();
    } catch (error) {
        console.error('Deploy error:', error);
    }
    hideLoading();
}

async function recallAsset(assetId) {
    showLoading();
    try {
        const response = await authenticatedFetch(`${API_BASE}/actions/recall`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ asset_id: assetId })
        });
        const result = await response.json();
        addActivity('resolve', result.result?.message || `Recalled ${assetId}`);
        loadData();
        map.closePopup();
    } catch (error) {
        console.error('Recall error:', error);
    }
    hideLoading();
}

async function resolveIncident(incidentId) {
    showLoading();
    try {
        const response = await authenticatedFetch(`${API_BASE}/actions/incident/${incidentId}/resolve`, { method: 'POST' });
        const result = await response.json();
        addActivity('resolve', result.result?.message || `Resolved ${incidentId}`);
        loadData();
        map.closePopup();
    } catch (error) {
        console.error('Resolve error:', error);
    }
    hideLoading();
}

async function createIncident() {
    const data = {
        type: document.getElementById('incident-type').value,
        priority: document.getElementById('incident-priority').value,
        description: document.getElementById('incident-description').value,
        affected_count: parseInt(document.getElementById('incident-affected').value) || 1,
        latitude: parseFloat(document.getElementById('incident-lat').value),
        longitude: parseFloat(document.getElementById('incident-lng').value)
    };

    if (!data.latitude || !data.longitude) {
        alert('Please click on the map to set incident location');
        return;
    }

    showLoading();
    try {
        const response = await authenticatedFetch(`${API_BASE}/actions/incident/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        addActivity('create', result.result?.message || 'Created new incident');
        closeModal('create-incident-modal');
        loadData();
    } catch (error) {
        console.error('Create error:', error);
    }
    hideLoading();
}

function showDeployModal(incidentId) {
    const modal = document.getElementById('deploy-modal');
    const select = document.getElementById('deploy-asset-select');
    const info = document.getElementById('deploy-target-info');

    const available = assets.filter(a => a.status === 'available');
    select.innerHTML = available.map(a => `<option value="${a.id}">${a.name} (${formatAssetType(a.type)})</option>`).join('');
    info.textContent = `Deploy to incident ${incidentId}`;

    document.getElementById('btn-confirm-deploy').onclick = () => {
        deployAsset(select.value, incidentId);
        closeModal('deploy-modal');
    };

    modal.classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    creatingIncident = false;
}

// ====== AI CHAT ======
// ====== COMMAND BAR ======
async function handleCommand(text) {
    const parts = text.slice(1).trim().split(/\s+/);
    const command = parts[0].toLowerCase();
    const args = parts.slice(1);

    addActivity('command', `Executing: ${text}`);

    if (command === 'help') {
        const helpText = `
            <strong>Available Commands:</strong><br>
            /deploy [asset_id] [incident_id] - Deploy asset<br>
            /recall [asset_id] - Recall asset<br>
            /resolve [incident_id] - Resolve incident<br>
            /help - Show this message
        `;
        document.getElementById('ai-response').classList.add('active');
        document.getElementById('ai-response').innerHTML = helpText;
        return;
    }

    try {
        if (command === 'deploy') {
            if (args.length < 2) throw new Error('Usage: /deploy [asset_id] [incident_id]');
            await deployAsset(args[0], args[1]);
        } else if (command === 'recall') {
            if (args.length < 1) throw new Error('Usage: /recall [asset_id]');
            await recallAsset(args[0]);
        } else if (command === 'resolve') {
            if (args.length < 1) throw new Error('Usage: /resolve [incident_id]');
            await resolveIncident(args[0]);
        } else {
            throw new Error(`Unknown command: ${command}`);
        }
    } catch (error) {
        document.getElementById('ai-response').classList.add('active');
        document.getElementById('ai-response').innerHTML = `<p style="color: var(--danger);">Error: ${error.message}</p>`;
        setTimeout(() => document.getElementById('ai-response').classList.remove('active'), 5000);
    }
}

// ====== AI CHAT ======
async function sendAIMessage(message) {
    // Check for slash command
    if (message.startsWith('/')) {
        handleCommand(message);
        return;
    }

    const responseEl = document.getElementById('ai-response');
    const input = document.getElementById('ai-chat-input');

    // Show response area with typing indicator
    responseEl.classList.add('active');
    responseEl.innerHTML = '<p class="typing">Thinking</p>';
    input.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/ai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, context: { incidents: incidents.slice(0, 5), assets: assets.slice(0, 5) } })
        });

        const data = await response.json();
        responseEl.innerHTML = `<p>${data.response || data.error || 'No response'}</p>`;

        if (data.computation_ms) {
            responseEl.innerHTML += `<small style="color: var(--text-muted); font-size: 0.7rem;">⚡ ${data.computation_ms}ms</small>`;
        }

        addActivity('system', `AI: ${(data.response || '').slice(0, 50)}...`);
    } catch (error) {
        responseEl.innerHTML = `<p style="color: var(--danger);">Error: ${error.message}</p>`;
    }

    input.disabled = false;
    input.focus();

    // Auto-hide after 10 seconds
    setTimeout(() => {
        if (responseEl.classList.contains('active')) {
            responseEl.classList.remove('active');
        }
    }, 10000);
}

// ====== ACTIVITY FEED ======
async function loadActivityLog() {
    try {
        const response = await fetch(`${API_BASE}/actions/log?limit=10`);
        const data = await response.json();
        const feed = document.getElementById('activity-feed');

        if (data.actions.length > 0) {
            feed.innerHTML = data.actions.reverse().map(action => {
                const time = new Date(action.executed_at || action.created_at).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
                const type = action.type.replace('_', ' ');
                return `<div class="activity-item ${action.type.split('_')[0]}">
                    <span class="activity-time">${time}</span>
                    <span class="activity-text">${action.result?.message || type}</span>
                </div>`;
            }).join('');
        }
    } catch (error) { }
}

function addActivity(type, message) {
    const feed = document.getElementById('activity-feed');
    const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
    const item = document.createElement('div');
    item.className = `activity-item ${type}`;
    item.innerHTML = `<span class="activity-time">${time}</span><span class="activity-text">${message}</span>`;
    feed.insertBefore(item, feed.firstChild);
    while (feed.children.length > 10) feed.removeChild(feed.lastChild);
}

// ====== AGENT COLLABORATION ======
async function startAgentCollaboration() {
    const btn = document.getElementById('btn-start-agents');
    const messagesContainer = document.getElementById('agent-messages');

    if (agentSessionActive) {
        stopAgentCollaboration();
        return;
    }

    agentSessionActive = true;
    btn.innerHTML = '<span>⏹ Stop</span>';
    messagesContainer.innerHTML = '';
    totalMessages = 0;
    totalComputationMs = 0;
    updateAgentMetrics();

    await fetch(`${API_BASE}/ai/agents/start`, { method: 'POST' });
    runAgentRound();
}

async function runAgentRound() {
    if (!agentSessionActive) return;
    try {
        const response = await fetch(`${API_BASE}/ai/agents/collaborate`, { method: 'POST' });
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const text = decoder.decode(value);
            const lines = text.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try { handleAgentEvent(JSON.parse(line.slice(6))); } catch (e) { }
                }
            }
        }
        if (agentSessionActive) setTimeout(() => runAgentRound(), 3000);
    } catch (error) { console.error('Agent error:', error); }
}

function handleAgentEvent(event) {
    if (event.type === 'agent_status') updateAgentStatus(event.agent, event.status);
    else if (event.type === 'agent_message') addAgentMessage(event.message);
}

function updateAgentStatus(agentId, status) {
    const avatar = document.querySelector(`.agent-avatar[data-agent="${agentId}"]`);
    if (!avatar) return;
    const statusEl = avatar.querySelector('.agent-status');
    if (status === 'thinking') { avatar.classList.add('thinking'); statusEl.textContent = 'thinking...'; }
    else { avatar.classList.remove('thinking'); statusEl.textContent = 'idle'; }
}

function addAgentMessage(message) {
    const container = document.getElementById('agent-messages');
    const agentId = message.from_agent;
    const color = AGENT_COLORS[agentId] || '#3b82f6';
    const name = AGENT_NAMES[agentId] || agentId;
    const icon = ICONS[agentId] || ICONS.command_agent;

    totalMessages++;
    totalComputationMs += message.computation_ms;
    updateAgentMetrics();

    const msgEl = document.createElement('div');
    msgEl.className = `agent-message ${agentId}`;
    msgEl.innerHTML = `
        <div class="message-avatar" style="border: 2px solid ${color};">${icon}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-agent" style="color: ${color};">${name}</span>
                <span class="message-time">${message.computation_ms}ms</span>
            </div>
            <div class="message-text">${(message.content || '').slice(0, 150)}</div>
        </div>
    `;
    container.appendChild(msgEl);
    container.scrollTop = container.scrollHeight;
    while (container.children.length > 10) container.removeChild(container.firstChild);
}

function updateAgentMetrics() {
    document.getElementById('metric-messages').textContent = totalMessages;
    const avgEl = document.getElementById('metric-avg-time');
    const avg = totalMessages > 0 ? Math.round(totalComputationMs / totalMessages) : 0;
    avgEl.textContent = avg;
    avgEl.className = 'metric-value' + (avg < 100 ? ' fast' : '');
    document.getElementById('metric-total-time').textContent = totalComputationMs;
}

function stopAgentCollaboration() {
    agentSessionActive = false;
    document.getElementById('btn-start-agents').innerHTML = '<span>▶ Start</span>';
    document.querySelectorAll('.agent-avatar').forEach(a => { a.classList.remove('thinking'); a.querySelector('.agent-status').textContent = 'idle'; });
    fetch(`${API_BASE}/ai/agents/stop`, { method: 'POST' });
}

// ====== AGENT GRAPH VISUALIZER ======
class AgentGraphVisualizer {
    constructor() {
        this.container = document.getElementById('agent-workflow-graph');
        this.modal = document.getElementById('agent-graph-modal');
        this.positions = {
            center: { x: 400, y: 300 },
            analyst: { x: 400, y: 100 },
            triage: { x: 650, y: 200 },
            resources: { x: 650, y: 400 },
            routing: { x: 400, y: 500 },
            command: { x: 150, y: 300 }
        };
        this.nodes = {};
        this.render();
    }

    render() {
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");
        svg.setAttribute("id", "agent-workflow-svg");
        svg.setAttribute("viewBox", "0 0 800 600");
        this.container.innerHTML = '';
        this.container.appendChild(svg);

        // Define gradients and filters
        const defs = document.createElementNS(svgNS, "defs");
        defs.innerHTML = `
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        `;
        svg.appendChild(defs);

        // Draw connections first (so they are behind nodes)
        const connectionsGroup = document.createElementNS(svgNS, "g");
        connectionsGroup.setAttribute("class", "connections");
        svg.appendChild(connectionsGroup);

        // Connections from Command (Hub) to everyone else
        const agents = ['analyst', 'triage', 'resources', 'routing'];
        agents.forEach(agent => {
            this.drawConnection(connectionsGroup, 'command', agent);
        });

        // Draw Nodes
        const nodesGroup = document.createElementNS(svgNS, "g");
        nodesGroup.setAttribute("class", "nodes");
        svg.appendChild(nodesGroup);

        this.drawNode(nodesGroup, 'command_agent', this.positions.command, 'Command', 'Orchestrator');
        this.drawNode(nodesGroup, 'situation_analyst', this.positions.analyst, 'Analyst', 'Situation Awareness');
        this.drawNode(nodesGroup, 'triage_agent', this.positions.triage, 'Triage', 'Priority & Risk');
        this.drawNode(nodesGroup, 'resource_coordinator', this.positions.resources, 'Resources', 'Asset Mgmt');
        this.drawNode(nodesGroup, 'routing_agent', this.positions.routing, 'Routing', 'Pathfinding');
    }

    drawNode(parent, id, pos, label, sub) {
        const svgNS = "http://www.w3.org/2000/svg";
        const group = document.createElementNS(svgNS, "g");
        group.setAttribute("class", "node-group");
        group.setAttribute("transform", `translate(${pos.x}, ${pos.y})`);
        group.setAttribute("data-agent", id);
        group.setAttribute("data-type", id);

        // Node Background
        const rect = document.createElementNS(svgNS, "rect");
        rect.setAttribute("class", "node-bg");
        rect.setAttribute("x", "-80");
        rect.setAttribute("y", "-40");
        rect.setAttribute("width", "160");
        rect.setAttribute("height", "80");
        rect.setAttribute("rx", "16");
        group.appendChild(rect);

        // Icon circle
        const circle = document.createElementNS(svgNS, "circle");
        circle.setAttribute("class", "node-icon-bg");
        circle.setAttribute("cx", "-50");
        circle.setAttribute("cy", "0");
        circle.setAttribute("r", "20");
        group.appendChild(circle);

        // Icon SVG
        const iconGroup = document.createElementNS(svgNS, "g");
        iconGroup.setAttribute("class", "node-icon");
        iconGroup.setAttribute("transform", "translate(-60, -10) scale(0.8)"); // Center and scale
        // Get raw SVG string
        const iconSvg = ICONS[id] || ICONS.command_agent;
        // Naive parsing: just set innerHTML on a foreignObject or parse it
        // Better: extract paths. But simpler is innerHTML on a g if browser supports it (it does for SVG)

        // We need to parse the string into DOM
        const parser = new DOMParser();
        const doc = parser.parseFromString(iconSvg, "image/svg+xml");
        const svgNode = doc.documentElement;

        // Copy children to iconGroup
        while (svgNode.firstChild) {
            iconGroup.appendChild(svgNode.firstChild);
        }

        // Set proper size/viewbox if needed, or just let children render
        // Assuming icons are valid SVG paths
        group.appendChild(iconGroup);


        // Text
        const text = document.createElementNS(svgNS, "text");
        text.setAttribute("class", "node-label");
        text.setAttribute("x", "10");
        text.setAttribute("y", "-5");
        text.textContent = label;
        group.appendChild(text);

        const subText = document.createElementNS(svgNS, "text");
        subText.setAttribute("class", "node-sublabel");
        subText.setAttribute("x", "10");
        subText.setAttribute("y", "15");
        subText.textContent = sub;
        group.appendChild(subText);

        parent.appendChild(group);
        this.nodes[id] = group;
    }

    drawConnection(parent, startKey, endKey) {
        const svgNS = "http://www.w3.org/2000/svg";
        const start = this.positions[startKey];
        const end = this.positions[endKey];

        const path = document.createElementNS(svgNS, "path");
        const d = `M ${start.x} ${start.y} C ${(start.x + end.x) / 2} ${start.y}, ${(start.x + end.x) / 2} ${end.y}, ${end.x} ${end.y}`;

        path.setAttribute("d", d);
        path.setAttribute("class", "connector-path");
        path.setAttribute("id", `conn-${startKey}-${endKey}`);
        parent.appendChild(path);
    }

    activate(agentId) {
        const node = this.nodes[agentId];
        if (node) {
            node.classList.add('active');
            // If it's not command, light up connection to command
            const shortId = agentId.split('_')[0].replace('situation', 'analyst').replace('resource', 'resources').replace('command', 'command');

            if (shortId !== 'command') {
                const connId = `conn-command-${shortId}`;
                const conn = document.getElementById(connId);
                if (conn) {
                    conn.classList.add('active');
                    this.animatePacket(conn);
                }
            }
        }
    }

    deactivate(agentId) {
        const node = this.nodes[agentId];
        if (node) {
            node.classList.remove('active');
            const shortId = agentId.split('_')[0].replace('situation', 'analyst').replace('resource', 'resources').replace('command', 'command');
            if (shortId !== 'command') {
                const conn = document.getElementById(`conn-command-${shortId}`);
                if (conn) conn.classList.remove('active');
            }
        }
    }

    animatePacket(pathElement) {
        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.getElementById('agent-workflow-svg');

        const circle = document.createElementNS(svgNS, "circle");
        circle.setAttribute("r", "4");
        circle.setAttribute("class", "data-packet flowing");

        const animateMotion = document.createElementNS(svgNS, "animateMotion");
        animateMotion.setAttribute("dur", "1s");
        animateMotion.setAttribute("repeatCount", "1");
        animateMotion.setAttribute("fill", "freeze");

        const mpath = document.createElementNS(svgNS, "mpath");
        mpath.setAttributeNS("http://www.w3.org/1999/xlink", "href", `#${pathElement.id}`);

        animateMotion.appendChild(mpath);
        circle.appendChild(animateMotion);

        // Remove after animation
        animateMotion.onend = () => circle.remove();
        setTimeout(() => circle.remove(), 1000); // Fallback

        svg.appendChild(circle);
    }

    show() {
        this.modal.classList.add('active');
    }

    hide() {
        this.modal.classList.remove('active');
    }
}

let graphVisualizer;

// ====== EVENT LISTENERS ======
function initializeEventListeners() {
    graphVisualizer = new AgentGraphVisualizer();

    document.getElementById('btn-agent-graph').addEventListener('click', () => {
        graphVisualizer.show();
    });

    document.getElementById('close-graph-modal').addEventListener('click', () => {
        graphVisualizer.hide();
    });

    // ... existing event listeners ...
    document.getElementById('btn-start-agents').addEventListener('click', startAgentCollaboration);
    document.getElementById('btn-refresh').addEventListener('click', loadData);
    document.getElementById('btn-center').addEventListener('click', () => map.setView([27.95, -82.46], 12));

    document.getElementById('btn-incidents').addEventListener('click', (e) => {
        showIncidents = !showIncidents;
        e.target.closest('.control-btn').classList.toggle('active', showIncidents);
        updateMapMarkers();
    });

    document.getElementById('btn-assets').addEventListener('click', (e) => {
        showAssets = !showAssets;
        e.target.closest('.control-btn').classList.toggle('active', showAssets);
        updateMapMarkers();
    });

    // Create Incident Modal
    document.getElementById('btn-add-incident').addEventListener('click', () => {
        creatingIncident = true;
        document.getElementById('create-incident-modal').classList.add('active');
    });
    document.getElementById('close-incident-modal').addEventListener('click', () => closeModal('create-incident-modal'));
    document.getElementById('btn-create-incident').addEventListener('click', createIncident);

    // Deploy Modal
    document.getElementById('close-deploy-modal').addEventListener('click', () => closeModal('deploy-modal'));

    // AI Chat
    document.getElementById('ai-chat-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.value.trim()) {
            sendAIMessage(e.target.value);
            e.target.value = '';
        }
    });
    document.getElementById('ai-send-btn').addEventListener('click', () => {
        const input = document.getElementById('ai-chat-input');
        if (input.value.trim()) {
            sendAIMessage(input.value);
            input.value = '';
        }
    });
}

// Update handleAgentEvent to trigger visualizer
const originalHandleAgentEvent = handleAgentEvent;
handleAgentEvent = function (event) {
    originalHandleAgentEvent(event);

    if (graphVisualizer) {
        if (event.type === 'agent_status') {
            if (event.status === 'thinking') {
                graphVisualizer.activate(event.agent);
            } else {
                graphVisualizer.deactivate(event.agent);
            }
        } else if (event.type === 'agent_message') {
            // flash the agent
            graphVisualizer.activate(event.message.from_agent);
            setTimeout(() => graphVisualizer.deactivate(event.message.from_agent), 1000);
        }
    }
};

// ====== UTILITIES ======
function showLoading() { document.getElementById('loading-overlay').classList.add('active'); }
function hideLoading() { document.getElementById('loading-overlay').classList.remove('active'); }
function startClock() { const update = () => { document.getElementById('current-time').textContent = new Date().toLocaleTimeString('en-US', { hour12: false }); }; update(); setInterval(update, 1000); }
async function checkAIStatus() { try { const res = await fetch(`${API_BASE}/ai/status`); const data = await res.json(); const dot = document.querySelector('#ai-status .status-dot'); const text = document.querySelector('#ai-status .status-text'); if (data.configured) { dot.style.background = '#10b981'; text.textContent = 'AI Ready'; } else { dot.style.background = '#f59e0b'; text.textContent = 'Demo Mode'; } } catch (e) { } }
function formatIncidentType(type) { return { flood_rescue: 'Flood Rescue', medical_emergency: 'Medical Emergency', structural_collapse: 'Structural Collapse', evacuation: 'Evacuation', utility_failure: 'Utility Failure', road_blockage: 'Road Blockage' }[type] || type; }
function formatAssetType(type) { return { boat: 'Rescue Boat', helicopter: 'Helicopter', ground_vehicle: 'Ground Vehicle', drone: 'Drone', medical_team: 'Medical Team', rescue_team: 'Rescue Team' }[type] || type; }
function getPriorityColor(p) { return { critical: '#ef4444', high: '#f97316', medium: '#eab308', low: '#22c55e' }[p] || '#64748b'; }
function getStatusColor(s) { return { available: '#22c55e', deployed: '#3b82f6', en_route: '#eab308', on_scene: '#f97316' }[s] || '#64748b'; }

