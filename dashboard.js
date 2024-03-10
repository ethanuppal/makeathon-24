// Copyright (C) 2024 Ethan Uppal. All rights reserved.

class Dashboard {
    constructor(element) {
        self.element = element;
    }

    configure() {
        if (!('DashboardConfig' in window)) {
            window.DashboardConfig = {};
        }
        if (!('source' in DashboardConfig)) {
            DashboardConfig.source = "static.json";
        }
        if (!('rate' in DashboardConfig)) {
            DashboardConfig.rate = 1;
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
                console.error('There was a problem fetching the data:', error);
                return null;
            }
        }
        const intervalId = setInterval(function () {
            fetchJSON(DashboardConfig.source)
                .then(data => {
                    if (data) {
                        update(data)
                    }
                });
        }, DashboardConfig.rate * 1000 /* milliseconds -> seconds */);
    }

    update(data) {
        if (!('version' in data)) {
            console.error('Unknown source format');
        }
        switch (data.version) {
            case 1: {
                updateV1(data.package);
                break;
            }
            default: {
                console.error('Unknown source version: ', data.version)
            }
        }
    }

    updateV1(package) {
        this.element.innerHTML = '<ul>' + [1, 2, 3, 4, 5]
            .map(level => (level, package.happiness["" + level]))
            .map((level, count) => `<li>level=${level} -> count=${count}</li>`) + '</ul>';
    }
}

window.addEventListener('load', function () {
    let dashboard = Dashboard(document.getElementById('telemetry-dashboard'));
    dashboard.configure();
    dashboard.run();
}, false);
