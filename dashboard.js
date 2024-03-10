// Copyright (C) 2024 Ethan Uppal. All rights reserved.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js'
import { getFirestore, onSnapshot, doc } from 'https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js'

class Dashboard {
    constructor(dashboardRootId) {
        this.dashboardRoot = document.getElementById(dashboardRootId);
        this.setupHTML();

        const firebaseConfig = {
            apiKey: "AIzaSyDyiPg6Dv_bJtCF_gettCwfTtSNFbibu3s",
            authDomain: "makeathon-24.firebaseapp.com",
            projectId: "makeathon-24",
            storageBucket: "makeathon-24.appspot.com",
            messagingSenderId: "997756541374",
            appId: "1:997756541374:web:0e850aa65a2919beaa81ef"
        };

        this.app = initializeApp(firebaseConfig);
        this.db = getFirestore(this.app);

        this.run();
    }

    setupHTML() {
        this.canvas = document.createElement('canvas');
        this.dashboardRoot.appendChild(this.canvas);

        this.dashboardRoot.style.width = '100%';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.display = 'block';
    }

    run() {
        onSnapshot(doc(this.db, "happiness", "current"), (doc) => {
            console.log(doc.data())
            this.update(doc.data())
        });
    }

    update(data) {
        if (!('version' in data)) {
            console.error('Unknown source format');
            return;
        }

        switch (data.version) {
            case 1: {
                this.updateV1(data.contents);
                break;
            }
            default: {
                console.error('Unknown source version: ', data.version)
            }
        }
    }

    updateV1(contents) {
        const ctx = this.canvas.getContext("2d");
        const width = this.canvas.width;
        const height = this.canvas.height;

        // blank slate
        ctx.clearRect(0, 0, width, height);

        const levels = [1, 2, 3, 4, 5];
        const colors = ['#ff0000', '#ff8000', '#80ff00', '#40ff00', '#00ff00'];
        const counts = levels.map(level => contents[`${level}`]);
        const levelTextRects = levels.map(level => ctx.measureText(`${level} (${counts[level - 1]})`));

        const textHeight = 10;

        const numColumns = levels.length;
        const columnWidth = width / numColumns;

        const maxCount = counts.reduce((x, y) => Math.max(x, y), 0);
        const heightPerCount = height / maxCount;

        for (let i = 0; i < numColumns; i++) {
            ctx.fillStyle = colors[i];
            const columnHeight = heightPerCount * counts[i];
            ctx.fillRect(i * columnWidth, height - columnHeight, columnWidth, columnHeight);

            ctx.font = `${textHeight}px Arial`;
            ctx.fillStyle = 'black';
            ctx.fillText(`${i + 1} (${counts[i]})`, (i + 0.5) * columnWidth - levelTextRects[i].width / 2, height - textHeight / 2);
        }
    }

    updateSource(newSource) {
        this.source = newSource;
        this.sourceInput.value = '';
        this.sourceSpan.textContent = newSource;
    }
}

window.addEventListener('load', function () {
    new Dashboard(
        'telemetry-dashboard',
    );
}, false);
