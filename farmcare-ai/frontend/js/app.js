// Shared state
const State = {
    myCrop: null,
    latestReport: null,
    imageURL: null, // to show image preview in report
    async loadMyCrop() {
        if(!this.myCrop) {
            this.myCrop = await API.getMyCrop();
        }
    }
};

let CropsList = [];

// Fetch crops from backend on load
let cropsPromise = (async function loadCrops() {
    try {
        const res = await fetch('/api/crops');
        const cropNames = await res.json();
        const emojis = {
            "Apple": "🍎", "Blueberry": "🫐", "Cherry (Including Sour)": "🍒",
            "Corn (Maize)": "🌽", "Grape": "🍇", "Orange": "🍊",
            "Peach": "🍑", "Pepper, Bell": "🫑", "Potato": "🥔",
            "Raspberry": "🍓", "Soybean": "🌱", "Squash": "🎃",
            "Strawberry": "🍓", "Tomato": "🍅"
        };
        CropsList = cropNames.map(name => ({
            id: name,
            emoji: emojis[name] || "🌿"
        }));
    } catch (e) {
        console.error("Failed to load crops", e);
    }
})();

function updateNavChip() {
    const chip = document.getElementById('nav-chip');
    if(State.latestReport) {
        const crop = CropsList.find(c => c.id === State.latestReport.crop);
        chip.innerHTML = `${crop?.emoji || ''} ${State.latestReport.crop} &middot; ${State.latestReport.status}`;
        chip.classList.remove('hidden');
    } else {
        chip.classList.add('hidden');
    }
}
