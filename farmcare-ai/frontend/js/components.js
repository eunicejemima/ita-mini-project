const Components = {
    renderHome() {
        return `
            <div class="container">
                <div class="hero">
                    <h1>Smart decisions. Healthier crops.</h1>
                    <p>Your Context-Aware AI Farm Action Planner.</p>
                    <br><br>
                    <a href="#/check" class="btn btn-primary" style="background:white; color:var(--primary-green)">📷 Check My Crop</a>
                </div>
                
                <h2 style="text-align:center; margin-bottom:30px;">How it works</h2>
                <div class="grid-3">
                    <div class="card" style="text-align:center">
                        <h1 style="font-size:3rem; margin:0">1️⃣</h1>
                        <h3>Upload</h3><p>Take a picture of a leaf.</p>
                    </div>
                    <div class="card" style="text-align:center">
                        <h1 style="font-size:3rem; margin:0">2️⃣</h1>
                        <h3>AI Analysis</h3><p>Our model analyzes it.</p>
                    </div>
                    <div class="card" style="text-align:center">
                        <h1 style="font-size:3rem; margin:0">3️⃣</h1>
                        <h3>Action Plan</h3><p>Get tailored recommendations.</p>
                    </div>
                </div>
            </div>
        `;
    },

    async renderMyCrop() {
        await State.loadMyCrop();
        await cropsPromise;
        const mc = State.myCrop || {};
        return `
            <div class="container grid-2">
                <div class="card">
                    <h2>🌱 My Crop Profile</h2>
                    <form id="my-crop-form">
                        <div class="input-group">
                            <label>Crop</label>
                            <select id="mc-crop">
                                ${CropsList.filter(c=>!c.disabled).map(c => `<option value="${c.id}" ${mc.crop===c.id?'selected':''}>${c.emoji} ${c.id.replace(/_/g, ' ')}</option>`).join('')}
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Crop Age (days)</label>
                            <input type="number" id="mc-age" value="${mc.age||30}">
                        </div>
                        <div class="input-group">
                            <label>Recent Rain</label>
                            <select id="mc-rain">
                                ${['Today','1–3 days ago','4–7 days ago','More than 7 days ago'].map(o => `<option ${mc.recent_rain===o?'selected':''}>${o}</option>`).join('')}
                            </select>
                        </div>
                        <div class="input-group">
                            <label>Soil Condition</label>
                            <select id="mc-soil">
                                ${['Wet','Normal','Dry'].map(o => `<option ${mc.soil===o?'selected':''}>${o}</option>`).join('')}
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Save Crop Profile</button>
                    </form>
                </div>
                <div>
                    <div class="card" style="background:var(--light-green); border-left:5px solid var(--primary-green)">
                        <h2>Your Saved Crop</h2>
                        <p><strong>Crop:</strong> <span id="lbl-crop">${mc.crop||'-'}</span></p>
                        <p><strong>Age:</strong> <span id="lbl-age">${mc.age||'-'}</span> days</p>
                        <p><strong>Rain:</strong> <span id="lbl-rain">${mc.recent_rain||'-'}</span></p>
                        <p><strong>Soil:</strong> <span id="lbl-soil">${mc.soil||'-'}</span></p>
                    </div>
                    <a href="#/check" class="btn btn-outline" style="width:100%; text-align:center">Check my crop with AI →</a>
                </div>
            </div>
        `;
    },

    async renderCheck() {
        await State.loadMyCrop();
        await cropsPromise;
        let html = `
            <div class="container">
                <div class="card" style="position:relative;">
                    <div class="demo-badge" id="demo-badge" style="display:none;">Demo Mode: predictions are simulated</div>
                    <div class="wizard-nav">
                        <span class="wizard-step active">① Select Crop</span>
                        <span class="wizard-step">② Upload</span>
                        <span class="wizard-step">③ Questions</span>
                        <span class="wizard-step">④ Results</span>
                    </div>
                    
                    <div id="step-1">
                        <h3>Choose a crop</h3>
                        <div class="grid-4">
                            ${CropsList.map(c => `
                                <div class="crop-card ${c.disabled?'disabled':''} ${State.myCrop?.crop===c.id?'active':''}" onclick="${c.disabled?'':'selectCrop(this, \''+c.id+'\')'}">
                                    <div style="font-size:2rem">${c.emoji}</div>
                                    <div style="font-weight:600">${c.id.replace('_', ' ')}${c.disabled?'<br><small>Coming soon</small>':''}</div>
                                </div>
                            `).join('')}
                        </div>
                        <br><button onclick="nextStep(2)" class="btn btn-primary">Next: Upload Image →</button>
                    </div>

                    <div id="step-2" class="hidden">
                        <h3>Upload Leaf Image</h3>
                        <div class="dropzone" id="dropzone">
                            <h2 style="margin:0">📸</h2>
                            <p>Click to upload or drag & drop a clear picture of a single leaf.</p>
                            <input type="file" id="file-input" style="display:none" accept="image/*">
                        </div>
                        <div id="preview-container" class="hidden" style="text-align:center; margin-top:20px;">
                            <img id="img-preview" src="" style="max-height:200px; border-radius:12px;">
                            <br><button onclick="document.getElementById('file-input').click()" class="btn btn-outline btn-sm" style="margin-top:10px">Change Image</button>
                        </div>
                        <br>
                        <button onclick="nextStep(1)" class="btn btn-outline">← Back</button>
                        <button onclick="nextStep(3)" class="btn btn-primary">Next: Questions →</button>
                    </div>

                    <div id="step-3" class="hidden">
                        <h3>Context Questions</h3>
                        <div class="input-group">
                            <label>🌧️ Has it rained recently?</label>
                            <div class="pills" id="pill-rain">
                                ${['Today','1–3 days ago','4–7 days ago','More than 7 days ago'].map(o => `<div class="pill ${State.myCrop?.recent_rain===o?'active':''}" onclick="togglePill(this, 'pill-rain')">${o}</div>`).join('')}
                            </div>
                        </div>
                        <div class="input-group">
                            <label>💧 How does the soil look?</label>
                            <div class="pills" id="pill-soil">
                                ${['Wet','Normal','Dry'].map(o => `<div class="pill ${State.myCrop?.soil===o?'active':''}" onclick="togglePill(this, 'pill-soil')">${o}</div>`).join('')}
                            </div>
                        </div>
                        <div class="input-group">
                            <label>📅 How long have you noticed the problem?</label>
                            <div class="pills" id="pill-duration">
                                ${['Today','A few days','More than a week'].map((o,i) => `<div class="pill ${i===0?'active':''}" onclick="togglePill(this, 'pill-duration')">${o}</div>`).join('')}
                            </div>
                        </div>
                        <br>
                        <button onclick="nextStep(2)" class="btn btn-outline">← Back</button>
                        <button onclick="submitAnalysis()" class="btn btn-primary">Analyze My Crop →</button>
                    </div>
                    
                    <div id="step-4" class="hidden">
                        <div id="loading" style="text-align:center; padding:40px;">
                            <h2 class="spinner">⏳</h2>
                            <p>Analyzing your crop...</p>
                        </div>
                        <div id="results-content" class="hidden">
                            <!-- Injected by JS -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        return html;
    },
    
    renderReport() {
        const rep = State.latestReport;
        if(!rep) {
            return `
                <div class="container text-center">
                    <div class="card" style="text-align:center; padding:60px;">
                        <h2>No recent analysis found.</h2>
                        <p>Perform an AI Crop Check to generate your farm report.</p>
                        <br><a href="#/check" class="btn btn-primary">Start AI Crop Check</a>
                    </div>
                    <div id="history-section" class="card hidden">
                        <h3>Past Checks History</h3>
                        <canvas id="historyChart" style="max-height:300px; margin-bottom:20px;"></canvas>
                        <div id="history-table"></div>
                    </div>
                </div>
            `;
        }

        const badgeClass = rep.status.includes('Healthy') ? 'badge-Healthy' : (rep.status.includes('Urgent') ? 'badge-Urgent' : 'badge-Attention');
        
        return `
            <div class="container">
                <div class="grid-2">
                    <div class="card">
                        ${State.imageURL ? `<img src="${State.imageURL}" style="width:100%; border-radius:12px; margin-bottom:20px">` : ''}
                        <h3>Crop: ${rep.crop}</h3>
                        <p><strong>Possible Indication:</strong> ${rep.prediction}</p>
                        <p><strong>Confidence:</strong> ${rep.confidence}%</p>
                        <span class="badge ${badgeClass}">${rep.status}</span>
                        <hr>
                        <p><strong>Context:</strong> Rain: ${rep.rain} | Soil: ${rep.soil} | Duration: ${rep.duration}</p>
                    </div>
                    <div>
                        <div class="card">
                            <h3>What should you do next?</h3>
                            ${rep.actions.map((a,i) => `<p><strong>0${i+1}.</strong> ${a}</p>`).join('')}
                        </div>
                        <div class="card">
                            <h3>Things to Inspect</h3>
                            <p>🔍 ${rep.things_to_inspect || 'No specific inspections.'}</p>
                        </div>
                        <div class="card">
                            <h3>Monitor these signs</h3>
                            <p>👀 ${rep.monitor_signs}</p>
                        </div>
                        <div class="card" style="border:2px solid var(--accent-amber)">
                            <h3>Need expert help?</h3>
                            <p>🧑‍🌾 ${rep.expert_help}</p>
                        </div>
                    </div>
                </div>
                <div class="text-center" style="margin-top:20px; text-align:center">
                    <a href="#/check" class="btn btn-primary">Check Another Leaf</a>
                </div>
                
                <div id="history-section" class="card mt-4" style="margin-top:24px;">
                    <h3>Past Checks History</h3>
                    <canvas id="historyChart" style="max-height:300px; margin-bottom:20px;"></canvas>
                    <div id="history-table"></div>
                </div>
            </div>
        `;
    }
};
