const Router = {
    async route() {
        const hash = window.location.hash || '#/home';
        const content = document.getElementById('app-content');
        
        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.nav-link[data-route="${hash.substring(1)}"]`);
        if(activeLink) activeLink.classList.add('active');

        if(hash === '#/home') content.innerHTML = Components.renderHome();
        else if(hash === '#/my-crop') {
            content.innerHTML = await Components.renderMyCrop();
            bindMyCropForm();
        }
        else if(hash === '#/check') {
            content.innerHTML = await Components.renderCheck();
            bindCheckWizard();
        }
        else if(hash === '#/report') {
            content.innerHTML = Components.renderReport();
            loadHistory();
        }
        else if(hash === '#/guide') {
            await cropsPromise;
            const cropsHtml = CropsList.map(c => `<div class="card" style="margin-bottom:10px;"><h3>${c.emoji} ${c.id}</h3></div>`).join('');
            content.innerHTML = `<div class="container"><div class="card"><h2>📚 Crop Guide</h2><p>View detailed information for all ${CropsList.length} crops here.</p>${cropsHtml}<a href="#/check" class="btn btn-primary" style="margin-top:20px;">Check My Crop →</a></div></div>`;
        }
        else content.innerHTML = '<h2>404 - Not Found</h2>';
        
        updateNavChip();
    }
};

window.addEventListener('hashchange', Router.route);
window.addEventListener('load', Router.route);

// JS logic for forms and wizard
function bindMyCropForm() {
    const form = document.getElementById('my-crop-form');
    if(!form) return;
    form.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            crop: document.getElementById('mc-crop').value,
            age: parseInt(document.getElementById('mc-age').value),
            recent_rain: document.getElementById('mc-rain').value,
            soil: document.getElementById('mc-soil').value
        };
        await API.saveMyCrop(data);
        State.myCrop = data;
        document.getElementById('lbl-crop').innerText = data.crop;
        document.getElementById('lbl-age').innerText = data.age;
        document.getElementById('lbl-rain').innerText = data.recent_rain;
        document.getElementById('lbl-soil').innerText = data.soil;
        alert("Saved successfully!");
    };
}

let selectedCropForCheck = null;
function selectCrop(el, cropId) {
    document.querySelectorAll('.crop-card').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    selectedCropForCheck = cropId;
}

function nextStep(step) {
    if(step === 2 && !selectedCropForCheck) {
        // Find if one is active (pre-filled)
        const act = document.querySelector('.crop-card.active');
        if(!act) { alert("Please select a crop."); return; }
        // Fallback extract cropId from onclick
    }
    
    document.querySelectorAll('[id^="step-"]').forEach(d => d.classList.add('hidden'));
    document.getElementById(`step-${step}`).classList.remove('hidden');
    
    document.querySelectorAll('.wizard-step').forEach((s, i) => {
        if(i < step) s.classList.add('active');
        else s.classList.remove('active');
    });
}

function togglePill(el, groupId) {
    document.querySelectorAll(`#${groupId} .pill`).forEach(p => p.classList.remove('active'));
    el.classList.add('active');
}

function bindCheckWizard() {
    const dz = document.getElementById('dropzone');
    const fi = document.getElementById('file-input');
    const pc = document.getElementById('preview-container');
    const pr = document.getElementById('img-preview');
    
    if(!dz) return;
    
    // Default select crop if mycrop exists
    if(State.myCrop && State.myCrop.crop) {
        selectedCropForCheck = State.myCrop.crop;
    }
    
    // Click to upload
    dz.onclick = () => fi.click();
    
    fi.onchange = (e) => {
        if(e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (re) => {
                pr.src = re.target.result;
                State.imageURL = re.target.result;
                dz.classList.add('hidden');
                pc.classList.remove('hidden');
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    };
}

async function submitAnalysis() {
    const file = document.getElementById('file-input').files[0];
    if(!file) { alert("Please upload an image first."); nextStep(2); return; }
    
    if(!selectedCropForCheck) {
        const activeCard = document.querySelector('.crop-card.active');
        if(activeCard) selectedCropForCheck = activeCard.innerText.trim().split('\\n')[0].trim();
    }
    
    const rain = document.querySelector('#pill-rain .pill.active')?.innerText || "Today";
    const soil = document.querySelector('#pill-soil .pill.active')?.innerText || "Normal";
    const duration = document.querySelector('#pill-duration .pill.active')?.innerText || "Today";
    
    nextStep(4);
    
    const fd = new FormData();
    fd.append("crop", selectedCropForCheck);
    fd.append("rain", rain);
    fd.append("soil", soil);
    fd.append("duration", duration);
    fd.append("file", file);
    
    try {
        const res = await API.analyzeCrop(fd);
        State.latestReport = res;
        updateNavChip();
        
        if(res.is_demo) { document.getElementById('demo-badge').style.display = 'block'; }
        
        document.getElementById('loading').classList.add('hidden');
        const resContent = document.getElementById('results-content');
        resContent.classList.remove('hidden');
        
        const badgeClass = res.status.includes('Healthy') ? 'badge-Healthy' : (res.status.includes('Urgent') ? 'badge-Urgent' : 'badge-Attention');
        
        let warnHTML = '';
        if(res.confidence < 60) warnHTML += '<div class="card" style="background:#FFF9C4; color:#F9A825">⚠️ Unclear result. The AI is not confident. Please upload a clearer photo.</div>';
        
        let othersHTML = '';
        if(res.top_3 && res.top_3.length > 0) {
            othersHTML = `<p style="font-size:0.9rem; color:#666; margin-top:10px;"><em>Other possibilities: ${res.top_3.map(t => `${t.label.split(' - ').pop()} ${t.confidence}%`).join(', ')}</em></p>`;
        }
        
        resContent.innerHTML = `
            ${warnHTML}
            <div class="grid-2">
                <div class="card text-center">
                    <h3>Crop: ${res.crop}</h3>
                    <p><strong>Possible Indication:</strong> ${res.prediction}</p>
                    <p><strong>Confidence:</strong> ${res.confidence}%</p>
                    <span class="badge ${badgeClass}">${res.status}</span>
                    ${othersHTML}
                </div>
                <div class="card">
                    <h3>Actions</h3>
                    ${res.actions.slice(0,3).map((a,i) => `<p><strong>0${i+1}.</strong> ${a}</p>`).join('')}
                </div>
            </div>
            <a href="#/report" class="btn btn-primary">View Full Farm Report →</a>
        `;
    } catch(e) {
        console.error(e);
        alert("Error analyzing crop.");
        nextStep(3);
    }
}

async function loadHistory() {
    const hist = await API.getHistory();
    if(hist && hist.length > 0) {
        document.getElementById('history-section')?.classList.remove('hidden');
        
        // Render table
        let thtml = '<table style="width:100%; text-align:left; border-collapse:collapse;"><tr><th>Date</th><th>Crop</th><th>Prediction</th><th>Confidence</th></tr>';
        hist.slice(-5).reverse().forEach(r => {
            thtml += `<tr style="border-bottom:1px solid #eee"><td>${r.timestamp}</td><td>${r.crop}</td><td>${r.prediction}</td><td>${r.confidence}%</td></tr>`;
        });
        thtml += '</table>';
        document.getElementById('history-table').innerHTML = thtml;
        
        // Render chart
        const ctx = document.getElementById('historyChart');
        if(ctx) {
            const counts = {};
            hist.forEach(r => { counts[r.prediction] = (counts[r.prediction]||0)+1; });
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(counts),
                    datasets: [{
                        data: Object.values(counts),
                        backgroundColor: ['#2E7D32','#4CAF50','#81C784','#C8E6C9','#F9A825','#D32F2F']
                    }]
                }
            });
        }
    }
}
