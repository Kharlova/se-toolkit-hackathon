// API base URL
const API_BASE = '';

// State
let selectedPlantId = null;

// DOM Elements
const addPlantForm = document.getElementById('addPlantForm');
const plantsList = document.getElementById('plantsList');
const noPlantsMessage = document.getElementById('noPlantsMessage');
const waterModal = new bootstrap.Modal(document.getElementById('waterModal'));
const modalPlantName = document.getElementById('modalPlantName');
const confirmWaterBtn = document.getElementById('confirmWaterBtn');

// Load plants on page load
document.addEventListener('DOMContentLoaded', loadPlants);

// Add plant form submission
addPlantForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('plantName').value.trim();
    const frequency = parseInt(document.getElementById('wateringFrequency').value);
    
    if (!name || !frequency) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/plants`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, watering_frequency_days: frequency })
        });
        
        if (response.ok) {
            addPlantForm.reset();
            loadPlants();
        }
    } catch (error) {
        console.error('Error adding plant:', error);
    }
});

// Confirm water button
confirmWaterBtn.addEventListener('click', async () => {
    if (!selectedPlantId) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/plants/${selectedPlantId}/water`, {
            method: 'POST'
        });
        
        if (response.ok) {
            waterModal.hide();
            loadPlants();
        }
    } catch (error) {
        console.error('Error watering plant:', error);
    }
});

// Load and display plants
async function loadPlants() {
    try {
        const response = await fetch(`${API_BASE}/api/plants`);
        const plants = await response.json();
        
        if (plants.length === 0) {
            noPlantsMessage.classList.remove('hidden');
            plantsList.innerHTML = '';
            return;
        }
        
        noPlantsMessage.classList.add('hidden');
        renderPlants(plants);
    } catch (error) {
        console.error('Error loading plants:', error);
    }
}

// Render plants list
function renderPlants(plants) {
    plantsList.innerHTML = plants.map(plant => {
        let statusClass, statusText, statusBadgeClass;
        
        if (plant.is_overdue) {
            statusClass = 'overdue';
            statusText = `Overdue by ${Math.abs(plant.days_until_watering)} day(s)!`;
            statusBadgeClass = 'bg-danger';
        } else if (plant.days_until_watering === 0) {
            statusClass = 'due-today';
            statusText = 'Due today!';
            statusBadgeClass = 'bg-warning text-dark';
        } else {
            statusClass = 'good';
            statusText = `Next watering in ${plant.days_until_watering} day(s)`;
            statusBadgeClass = 'bg-success';
        }
        
        const lastWateredText = plant.last_watered 
            ? new Date(plant.last_watered).toLocaleDateString('en-US', { 
                year: 'numeric', month: 'short', day: 'numeric' 
            })
            : 'Never';
        
        return `
            <div class="col-md-6 col-lg-4">
                <div class="plant-item ${statusClass}">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <div class="plant-name">
                                <i class="bi bi-flower2 text-success"></i> ${escapeHtml(plant.name)}
                            </div>
                            <div class="watering-info">
                                <i class="bi bi-calendar-repeat"></i> Every ${plant.watering_frequency_days} day(s)
                            </div>
                        </div>
                        <span class="badge ${statusBadgeClass} status-badge">${statusText}</span>
                    </div>
                    <div class="text-muted small mb-3">
                        <i class="bi bi-droplet-half"></i> Last watered: ${lastWateredText}
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-success water-btn" onclick="openWaterModal(${plant.id}, '${escapeHtml(plant.name)}')">
                            <i class="bi bi-droplet"></i> Water
                        </button>
                        <button class="btn btn-outline-danger delete-btn" onclick="deletePlant(${plant.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Open water confirmation modal
function openWaterModal(plantId, plantName) {
    selectedPlantId = plantId;
    modalPlantName.textContent = plantName;
    waterModal.show();
}

// Delete plant
async function deletePlant(plantId) {
    if (!confirm('Are you sure you want to delete this plant?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/plants/${plantId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadPlants();
        }
    } catch (error) {
        console.error('Error deleting plant:', error);
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
