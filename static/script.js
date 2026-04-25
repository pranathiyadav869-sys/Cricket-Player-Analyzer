// static/script.js

// Global Chart variables to store instances
let analyzeRadarChart = null;
let viewRadarChart = null;
let compareRadarChart = null;

// --- Utility Functions ---

/**
 * Initializes or updates a Chart.js Radar Chart.
 */
function updateRadarChart(canvasId, labels, datasets, chartInstance) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    if (chartInstance) {
        chartInstance.destroy();
    }

    const newChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { display: false },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    pointLabels: { font: { size: 14 } },
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { position: 'top' },
                tooltip: { callbacks: { label: (context) => `${context.dataset.label}: ${context.raw.toFixed(1)}%` } }
            }
        }
    });

    return newChart;
}


/**
 * Updates player dropdowns on all tabs with the latest list of names.
 */
function updateDropdowns(playerNames) {
    const selects = ['view-select', 'compare-select1', 'compare-select2'];

    selects.forEach(id => {
        const select = document.getElementById(id);
        const currentValue = select.value;
        select.innerHTML = '<option value="">-- Select --</option>'; // Clear options
        
        playerNames.forEach(name => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            select.appendChild(option);
        });

        if (playerNames.includes(currentValue)) {
            select.value = currentValue;
        }
    });
    
    updatePlayerCheckboxes(playerNames, 'balance-player-list', 'balance-player-');
    updatePlayerCheckboxes(playerNames, 'selection-player-list', 'selection-player-');
}

/**
 * Populates a div with player checkboxes.
 */
function updatePlayerCheckboxes(playerNames, containerId, baseName) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';
    playerNames.forEach(name => {
        const div = document.createElement('div');
        div.className = 'player-checkbox-item';
        div.innerHTML = `
            <input type="checkbox" id="${baseName}${name}" name="player" value="${name}">
            <label for="${baseName}${name}">${name}</label>
        `;
        container.appendChild(div);
    });
}


// --- Tab: Add & Analyze Player (Unchanged) ---
document.getElementById('analyze-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const playerStats = Object.fromEntries(formData);
    const statusElement = document.getElementById('analyze-status');
    statusElement.textContent = 'Analyzing...';
    statusElement.style.color = 'orange';

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(playerStats),
        });

        const data = await response.json();

        if (data.status === 'success') {
            statusElement.textContent = `✅ Saved '${data.player_name}' as ${data.role}`;
            statusElement.style.color = 'green';
            
            document.getElementById('out-role').textContent = data.role;
            document.getElementById('out-perf').textContent = data.performance_score;
            document.getElementById('out-bat-cons').textContent = data.batting_consistency;
            document.getElementById('out-bowl-cons').textContent = data.bowling_consistency;

            const datasets = [{
                label: data.player_name,
                data: data.radar_data,
                backgroundColor: 'rgba(0, 137, 123, 0.2)',
                borderColor: 'rgba(0, 137, 123, 1)',
                pointBackgroundColor: 'rgba(0, 137, 123, 1)',
                borderWidth: 2
            }];
            analyzeRadarChart = updateRadarChart('analyzeRadarChart', data.radar_labels, datasets, analyzeRadarChart);
            
            updateDropdowns(data.all_player_names);

        } else {
            statusElement.textContent = `❌ Error: ${data.message}`;
            statusElement.style.color = 'red';
        }
    } catch (error) {
        statusElement.textContent = '❌ A network error occurred.';
        statusElement.style.color = 'red';
        console.error('Fetch error:', error);
    }
});


// --- Tab: View Player (Unchanged) ---
document.getElementById('view-select').addEventListener('change', async function() {
    const playerName = this.value;
    if (!playerName) return;

    try {
        const response = await fetch(`/api/player/${playerName}`);
        const data = await response.json();

        if (data.status === 'success') {
            const p = data.player_data;
            document.getElementById('view-player-name').textContent = playerName;
            document.getElementById('view-perf').textContent = data.performance_score;
            document.getElementById('view-bat-cons').textContent = data.batting_consistency;
            document.getElementById('view-bowl-cons').textContent = data.bowling_consistency;

            document.getElementById('view-stats-text').textContent = 
                `Matches: ${p.matches}\nBat Innings: ${p.bat_innings}\nRuns: ${p.bat_runs}\nHS: ${p.high_score}\n` +
                `Bat Avg: ${p.bat_avg}\nSR: ${p.bat_sr}\n50s: ${p.fifties}\n100s: ${p.hundreds}\n` +
                `Wickets: ${p.wickets}\nEcon: ${p.econ}\nBowl SR: ${p.bowl_sr}`;

            const datasets = [{
                label: playerName,
                data: data.radar_data,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }];
            viewRadarChart = updateRadarChart('viewRadarChart', data.radar_labels, datasets, viewRadarChart);

        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});


// --- Tab: Compare Players (Unchanged) ---
document.getElementById('compare-btn-all').addEventListener('click', async function() {
    const player1 = document.getElementById('compare-select1').value;
    const player2 = document.getElementById('compare-select2').value;
    const summaryElement = document.getElementById('compare-summary-all');

    if (!player1 || !player2) {
        alert("Please select two players for comparison.");
        return;
    }

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player1: player1, player2: player2 }),
        });

        const data = await response.json();

        if (data.status === 'success') {
            const datasets = [
                {
                    label: player1,
                    data: data.radar_data[player1],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                },
                {
                    label: player2,
                    data: data.radar_data[player2],
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    pointBackgroundColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 2
                }
            ];
            compareRadarChart = updateRadarChart('compareRadarChart', data.radar_labels, datasets, compareRadarChart);

            let summaryText = '';
            for (const [metric, result] of Object.entries(data.comparison_results)) {
                summaryText += 
                    `${metric.padEnd(13)}: ${player1}=${result[player1]} | ${player2}=${result[player2]} → Stronger: ${result.stronger}\n`;
            }
            summaryElement.textContent = summaryText;

        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});


// --- Initial Load (Unchanged) ---
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/players');
        if (response.ok) {
            const data = await response.json();
            updateDropdowns(data.all_player_names || []);
        }
    } catch (e) {
        console.warn("Could not fetch initial player list. Start adding players!");
    }
});

// --- Leaderboard Logic (Unchanged) ---
document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("leaderboard-role");
    const leaderboardContainer = document.getElementById("leaderboard-container");

    if (roleSelect) {
        roleSelect.addEventListener("change", async () => {
            const role = roleSelect.value;
            leaderboardContainer.innerHTML = "";

            if (!role) {
                leaderboardContainer.innerHTML = "<p>Please select a role to view leaderboard.</p>";
                return;
            }

            try {
                const res = await fetch(`/leaderboard_data?role=${role}`);
                const data = await res.json();

                if (!data.players || data.players.length === 0) {
                    leaderboardContainer.innerHTML = `<p class='status'>${data.message || "No players found."}</p>`;
                    return;
                }

                let html = `
                    <table class="leaderboard-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Player</th>
                                <th>Performance</th>
                                <th>Bat Consistency</th>
                                <th>Bowl Consistency</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                data.players.forEach((p, index) => {
                    html += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${p.name}</td>
                            <td>${p.performance_score.toFixed(2)}</td>
                            <td>${p.batting_consistency.toFixed(2)}</td>
                            <td>${p.bowling_consistency.toFixed(2)}</td>
                        </tr>
                    `;
                });

                html += `</tbody></table>`;
                leaderboardContainer.innerHTML = html;
            } catch (error) {
                leaderboardContainer.innerHTML = "<p class='status'>Error loading leaderboard.</p>";
                console.error(error);
            }
        });
    }
});

// ----------------------------
// --- Tab: Team Balance Analyzer Logic (Unchanged) ---

document.addEventListener("DOMContentLoaded", function () {
    const balanceForm = document.getElementById('balance-form');
    const balanceStatus = document.getElementById('balance-status');
    const balanceResultsBox = document.getElementById('balance-results-box');
    const balanceRating = document.getElementById('balance-rating');
    const balanceBatsmen = document.getElementById('balance-batsmen');
    const balanceBowlers = document.getElementById('balance-bowlers');
    const balanceAllrounders = document.getElementById('balance-allrounders');
    const balanceWK = document.getElementById('balance-wk');

    if (balanceForm) {
        balanceForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const selectedPlayers = Array.from(balanceForm.querySelectorAll('input[name="player"]:checked')).map(cb => cb.value);

            balanceResultsBox.style.display = 'none';
            balanceStatus.textContent = 'Analyzing balance...';
            balanceStatus.style.color = 'orange';

            if (selectedPlayers.length !== 11) {
                balanceStatus.textContent = `❌ Error: Please select exactly 11 players. (Selected: ${selectedPlayers.length})`;
                balanceStatus.style.color = 'red';
                return;
            }

            try {
                const response = await fetch('/api/team_balance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ players: selectedPlayers }),
                });

                const data = await response.json();

                if (data.status === 'success') {
                    const counts = data.counts;
                    balanceStatus.textContent = `✅ Balance Analysis Complete!`;
                    balanceStatus.style.color = 'green';
                    
                    balanceRating.innerHTML = data.rating;
                    balanceBatsmen.textContent = counts.Batsman;
                    balanceBowlers.textContent = counts.Bowler;
                    balanceAllrounders.textContent = counts.Allrounder;
                    balanceWK.textContent = counts.Wicketkeeper;
                    balanceResultsBox.style.display = 'flex';

                } else {
                    balanceStatus.textContent = `❌ Error: ${data.message}`;
                    balanceStatus.style.color = 'red';
                }
            } catch (error) {
                balanceStatus.textContent = '❌ A network error occurred.';
                balanceStatus.style.color = 'red';
                console.error('Fetch error:', error);
            }
        });
    }
});


// ----------------------------
// --- Team Generator Logic (Updated for Single Team Default) ---

function renderSingleTeam(teamData, statusElement) {
    const bestTeamContainer = document.getElementById("best-team-body");
    const bestTeamRating = document.getElementById("best-team-rating");
    const bestTeamComp = document.getElementById("best-team-comp");
    const bestTeamTotalPerf = document.getElementById("best-team-total-perf");

    bestTeamContainer.innerHTML = '';

    if (teamData.status !== 'success' || teamData.mode !== 'best_team') {
        statusElement.textContent = `❌ Error: ${teamData.message || "Failed to generate team."}`;
        statusElement.style.color = 'red';
        return;
    }

    const team = teamData.team;
    statusElement.textContent = `✅ Best team generated! Balance: ${team.rating}`;
    statusElement.style.color = 'green';
    
    bestTeamRating.innerHTML = team.rating;
    bestTeamTotalPerf.textContent = team.total_perf.toFixed(2);
    const counts = team.counts;
    bestTeamComp.textContent = `${counts.Batsman} | ${counts.Bowler} | ${counts.Allrounder} | ${counts.Wicketkeeper}`;

    team.players.forEach(p => {
        const row = bestTeamContainer.insertRow();
        row.insertCell().textContent = p.name;
        row.insertCell().textContent = p.role;
        row.insertCell().textContent = p.performance_score.toFixed(2);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    const generateBtnAll = document.getElementById("generate-teams-btn-all");
    const showSelectionBtn = document.getElementById("show-selection-btn");
    const selectionModeDiv = document.getElementById("selection-mode-div");
    const selectionForm = document.getElementById('selection-form');
    const statusElement = document.getElementById("team-status");
    

    function setMode(mode) {
        if (mode === 'all') {
            selectionModeDiv.style.display = 'none';
        } else if (mode === 'select') {
            selectionModeDiv.style.display = 'block';
        }
    }
    
    // Function to run the generation for ALL players (Default)
    const runDefaultGeneration = async () => {
        setMode('all');
        statusElement.textContent = 'Generating best team from ALL registered players...';
        statusElement.style.color = 'orange';

        try {
            const res = await fetch(`/api/teams`); // GET request
            const data = await res.json();
            renderSingleTeam(data, statusElement);
        } catch (error) {
            statusElement.textContent = '❌ A network error occurred.';
            statusElement.style.color = 'red';
            console.error('Fetch error:', error);
        }
    };
    
    // Toggle to selection mode
    if (showSelectionBtn) {
        showSelectionBtn.addEventListener('click', () => {
            setMode('select');
            statusElement.textContent = 'Selection mode active. Choose players and click generate.';
            statusElement.style.color = '#4dd0e1';
        });
    }

    // 1. Logic for Generate from ALL button (NEW DEFAULT)
    if (generateBtnAll) {
        generateBtnAll.addEventListener("click", runDefaultGeneration);
    }
    
    // 2. Logic for GENERATE BEST TEAM FROM SELECTION form (POST)
    if (selectionForm) {
        selectionForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            setMode('select');
            
            const selectedPlayers = Array.from(selectionForm.querySelectorAll('input[name="player"]:checked')).map(cb => cb.value);
            
            statusElement.textContent = 'Generating best team from selection...';
            statusElement.style.color = 'orange';
            
            if (selectedPlayers.length < 11) {
                statusElement.textContent = `❌ Error: Select at least 11 players for the selection process. (Selected: ${selectedPlayers.length})`;
                statusElement.style.color = 'red';
                return;
            }

            try {
                const res = await fetch(`/api/teams`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ players: selectedPlayers }),
                });

                const data = await res.json();
                renderSingleTeam(data, statusElement);

            } catch (error) {
                statusElement.textContent = '❌ A network error occurred.';
                statusElement.style.color = 'red';
                console.error('Fetch error:', error);
            }
        });
    }

    // Initial Generation on Load (Defaulting to ALL players)
    const tabTeams = document.getElementById('tab-teams');
    if (tabTeams && tabTeams.checked) {
        runDefaultGeneration();
    }
});