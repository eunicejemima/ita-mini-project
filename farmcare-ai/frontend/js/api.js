const API = {
    async getMyCrop() {
        const res = await fetch('/api/my-crop');
        return res.json();
    },
    async saveMyCrop(data) {
        const res = await fetch('/api/my-crop', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        return res.json();
    },
    async analyzeCrop(formData) {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        return res.json();
    },
    async getHistory() {
        const res = await fetch('/api/history');
        return res.json();
    }
};
