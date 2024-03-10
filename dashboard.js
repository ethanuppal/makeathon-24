// Copyright (C) 2024 Ethan Uppal. All rights reserved.

class Dashboard {
    constructor(dashboardRootId, sourceInputId, sourceButtonId, sourceSpanId) {
        this.dashboardRoot = document.getElementById(dashboardRootId);
        this.sourceInput = document.getElementById(sourceInputId);
        this.sourceButton = document.getElementById(sourceButtonId);
        this.sourceSpan = document.getElementById(sourceSpanId);
        this.setupHTML()
        this.configure();
        this.run();
    }

    setupHTML() {
        this.canvas = document.createElement('canvas');
        this.dashboardRoot.appendChild(this.canvas);

        this.dashboardRoot.style.width = '100%';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.display = 'block';

        this.sourceButton.addEventListener('click', () => {
            if (this.sourceInput.value.length > 0) {
                this.updateSource(this.sourceInput.value);
            }
        }, false);
    }

    configure() {
        if ('DashboardConfig' in window) {
            if (!('source' in DashboardConfig)) {
                this.updateSource('example/static_v1.json');
            } else {
                this.updateSource(DashboardConfig.source);
            }
            if (!('rate' in DashboardConfig)) {
                this.rate = 1;
            }
        }
    }

    run() {
        async function fetchJSON(url) {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return await response.json();
            } catch (error) {
                return null;
            }
        }

        const updateBound = this.update.bind(this);
        const intervalId = setInterval(() => {
            fetchJSON(this.source)
                .then(data => {
                    if (data) {
                        updateBound(data);
                        this.sourceSpan.style.color = 'black';
                    } else {
                        this.sourceSpan.style.color = 'red';
                    }
                })
        }, this.rate * 1000 /* milliseconds -> seconds */);
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
        const counts = levels.map(level => contents.happiness[`${level}`]);
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
        'source-url-input',
        'source-url-button',
        'source-url-span'
    );
}, false);
