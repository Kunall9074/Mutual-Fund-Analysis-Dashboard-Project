/* ═══════════════════════════════════════════════════════════
   MUTUAL FUND INSIGHTS DASHBOARD — APP LOGIC
   ═══════════════════════════════════════════════════════════ */

// ── GLOBALS ─────────────────────────────────────────────────
let DATA = null;
let ALL_FUNDS = [];
let FILTERED_FUNDS = [];
let CHARTS = {};

// ── CHART PALETTE ───────────────────────────────────────────
const PALETTE = [
    '#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e',
    '#8b5cf6', '#0ea5e9', '#f97316', '#ec4899', '#14b8a6',
    '#a855f7', '#eab308', '#3b82f6', '#ef4444', '#22c55e',
    '#e879f9', '#fbbf24', '#2dd4bf', '#fb923c', '#818cf8',
];

const PALETTE_ALPHA = PALETTE.map(c => c + '33');

// ── INIT ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadData();
});

async function loadData() {
    try {
        const response = await fetch('../data/dashboard_data.json');
        DATA = await response.json();
        ALL_FUNDS = DATA.all_funds;
        FILTERED_FUNDS = [...ALL_FUNDS];

        populateFilters();
        updateDashboard();
        setupEventListeners();

        // Header badge
        document.getElementById('headerBadge').textContent =
            `${DATA.kpis.total_funds} Schemes Analyzed`;

    } catch (err) {
        console.error('Failed to load data:', err);
        document.getElementById('headerBadge').textContent = 'Data Load Error';
    }
}

// ── FILTERS ─────────────────────────────────────────────────
function populateFilters() {
    const filters = DATA.filters;
    fillSelect('filterFundType', filters.fund_types);
    fillSelect('filterCategory', filters.categories);
    fillSelect('filterRisk', filters.risk_levels);
    fillSelect('filterAMC', filters.amc_names);
    fillSelect('filterRating', filters.fund_ratings.map(String));
}

function fillSelect(id, options) {
    const sel = document.getElementById(id);
    const defaultOpt = sel.options[0];
    sel.innerHTML = '';
    sel.appendChild(defaultOpt);
    options.forEach(opt => {
        const o = document.createElement('option');
        o.value = opt;
        o.textContent = opt;
        sel.appendChild(o);
    });
}

function setupEventListeners() {
    ['filterFundType', 'filterCategory', 'filterRisk', 'filterAMC', 'filterRating'].forEach(id => {
        document.getElementById(id).addEventListener('change', applyFilters);
    });
    document.getElementById('btnReset').addEventListener('click', resetFilters);

    // Table sorting
    document.querySelectorAll('.data-table thead th[data-sort]').forEach(th => {
        th.addEventListener('click', () => sortTable(th));
    });
}

function applyFilters() {
    const fundType = document.getElementById('filterFundType').value;
    const category = document.getElementById('filterCategory').value;
    const riskLevel = document.getElementById('filterRisk').value;
    const amcName = document.getElementById('filterAMC').value;
    const rating = document.getElementById('filterRating').value;

    FILTERED_FUNDS = ALL_FUNDS.filter(f => {
        if (fundType && f['Fund Type'] !== fundType) return false;
        if (category && f['Category'] !== category) return false;
        if (riskLevel && f['Risk Level'] !== riskLevel) return false;
        if (amcName && f['AMC Name'] !== amcName) return false;
        if (rating && String(f['Fund Rating']) !== rating) return false;
        return true;
    });

    updateDashboard();
}

function resetFilters() {
    document.getElementById('filterFundType').value = '';
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterRisk').value = '';
    document.getElementById('filterAMC').value = '';
    document.getElementById('filterRating').value = '';
    FILTERED_FUNDS = [...ALL_FUNDS];
    updateDashboard();
}

// ── UPDATE DASHBOARD ────────────────────────────────────────
function updateDashboard() {
    updateKPIs();
    updateCharts();
    updateInsights();
    updateTable();
}

// ── KPIs ────────────────────────────────────────────────────
function updateKPIs() {
    const funds = FILTERED_FUNDS;
    const n = funds.length;

    animateValue('kpiTotalFunds', n, false);
    animateValue('kpiTotalAUM', Math.round(funds.reduce((s, f) => s + f['AUM (Cr)'], 0)), true);
    animateValue('kpiAvgReturn', n ? (funds.reduce((s, f) => s + f['Return 3Y (%)'], 0) / n).toFixed(1) : '0', false);
    animateValue('kpiExpenseRatio', n ? (funds.reduce((s, f) => s + f['Expense Ratio (%)'], 0) / n).toFixed(2) : '0', false);
    animateValue('kpiAvgSIP', n ? Math.round(funds.reduce((s, f) => s + f['Min SIP (₹)'], 0) / n) : 0, true);
}

function animateValue(id, endValue, isCurrency) {
    const el = document.getElementById(id);
    const numVal = parseFloat(String(endValue).replace(/,/g, ''));

    if (isNaN(numVal)) {
        el.textContent = endValue;
        return;
    }

    const duration = 600;
    const startTime = performance.now();
    const startVal = 0;

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = startVal + (numVal - startVal) * eased;

        if (isCurrency) {
            el.textContent = formatNumber(Math.round(current));
        } else {
            if (String(endValue).includes('.')) {
                el.textContent = current.toFixed(String(endValue).split('.')[1].length);
            } else {
                el.textContent = Math.round(current).toLocaleString('en-IN');
            }
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function formatNumber(num) {
    if (num >= 10000000) return (num / 10000000).toFixed(1) + ' Cr';
    if (num >= 100000) return (num / 100000).toFixed(1) + ' L';
    return num.toLocaleString('en-IN');
}

// ── CHARTS ──────────────────────────────────────────────────
function updateCharts() {
    updateReturnsCategoryChart();
    updateTopAMCsChart();
    updateAUMTypeChart();
    updateExpenseStrategyChart();
    updateFundManagersChart();
    updateRiskDistChart();
}

function destroyChart(key) {
    if (CHARTS[key]) {
        CHARTS[key].destroy();
        delete CHARTS[key];
    }
}

function updateReturnsCategoryChart() {
    destroyChart('returnsCategory');
    const groupedData = groupBy(FILTERED_FUNDS, 'Category', 'Return 3Y (%)', 'avg');
    const sorted = Object.entries(groupedData).sort((a, b) => b[1] - a[1]).slice(0, 12);

    const ctx = document.getElementById('chartReturnsCategory').getContext('2d');
    CHARTS.returnsCategory = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: sorted.map(d => d[0]),
            datasets: [{
                data: sorted.map(d => d[1]),
                backgroundColor: PALETTE.slice(0, sorted.length),
                borderColor: 'transparent',
                borderWidth: 0,
                hoverOffset: 12,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '55%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#94a3b8',
                        font: { family: 'Inter', size: 11 },
                        padding: 10,
                        boxWidth: 12,
                        boxHeight: 12,
                        borderRadius: 3,
                        useBorderRadius: true,
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    titleFont: { family: 'Inter', weight: '600' },
                    bodyFont: { family: 'Inter' },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `${ctx.label}: ${ctx.parsed.toFixed(1)}% avg return`
                    }
                }
            },
            animation: { animateRotate: true, duration: 800 }
        }
    });
}

function updateTopAMCsChart() {
    destroyChart('topAMCs');
    const groupedData = groupBy(FILTERED_FUNDS, 'AMC Name', 'Return 3Y (%)', 'avg');
    const sorted = Object.entries(groupedData).sort((a, b) => b[1] - a[1]).slice(0, 10);

    const ctx = document.getElementById('chartTopAMCs').getContext('2d');
    CHARTS.topAMCs = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(d => d[0].replace(' Mutual Fund', '')),
            datasets: [{
                label: 'Avg 3Y Return (%)',
                data: sorted.map(d => d[1]),
                backgroundColor: createGradientBars(ctx, sorted.length, '#6366f1', '#06b6d4'),
                borderRadius: 6,
                borderSkipped: false,
                barPercentage: 0.65,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', font: { family: 'Inter', size: 10 }, maxRotation: 45 },
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#64748b', font: { family: 'Inter', size: 11 }, callback: v => v + '%' },
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `Avg Return: ${ctx.parsed.y.toFixed(1)}%`
                    }
                }
            },
            animation: { duration: 800 }
        }
    });
}

function updateAUMTypeChart() {
    destroyChart('aumType');
    const groupedData = groupBy(FILTERED_FUNDS, 'Fund Type', 'AUM (Cr)', 'sum');
    const sorted = Object.entries(groupedData).sort((a, b) => b[1] - a[1]);

    const ctx = document.getElementById('chartAUMType').getContext('2d');
    CHARTS.aumType = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: sorted.map(d => d[0]),
            datasets: [{
                data: sorted.map(d => d[1]),
                backgroundColor: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e'],
                borderColor: 'transparent',
                hoverOffset: 12,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 }, padding: 10, boxWidth: 12, borderRadius: 3, useBorderRadius: true }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `${ctx.label}: ₹${formatNumber(Math.round(ctx.parsed))}`
                    }
                }
            },
            animation: { animateRotate: true, duration: 800 }
        }
    });
}

function updateExpenseStrategyChart() {
    destroyChart('expenseStrategy');
    const groupedData = groupBy(FILTERED_FUNDS, 'Investment Strategy', 'Expense Ratio (%)', 'avg');
    const sorted = Object.entries(groupedData).sort((a, b) => b[1] - a[1]);

    const ctx = document.getElementById('chartExpenseStrategy').getContext('2d');
    CHARTS.expenseStrategy = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(d => d[0]),
            datasets: [{
                label: 'Avg Expense Ratio (%)',
                data: sorted.map(d => d[1]),
                backgroundColor: createGradientBars(ctx, sorted.length, '#f43f5e', '#f59e0b'),
                borderRadius: 6,
                borderSkipped: false,
                barPercentage: 0.55,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } },
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#64748b', font: { family: 'Inter', size: 11 }, callback: v => v + '%' },
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `Expense Ratio: ${ctx.parsed.y.toFixed(2)}%`
                    }
                }
            },
            animation: { duration: 800 }
        }
    });
}

function updateFundManagersChart() {
    destroyChart('fundManagers');
    const groupedData = groupBy(FILTERED_FUNDS, 'Fund Manager', 'AUM (Cr)', 'sum');
    const sorted = Object.entries(groupedData).sort((a, b) => b[1] - a[1]).slice(0, 12);

    const ctx = document.getElementById('chartFundManagers').getContext('2d');
    CHARTS.fundManagers = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(d => d[0]),
            datasets: [{
                label: 'Total AUM (₹ Cr)',
                data: sorted.map(d => d[1]),
                backgroundColor: createGradientBars(ctx, sorted.length, '#8b5cf6', '#06b6d4'),
                borderRadius: 6,
                borderSkipped: false,
                barPercentage: 0.6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: {
                        color: '#64748b',
                        font: { family: 'Inter', size: 10 },
                        callback: v => formatNumber(v)
                    },
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } },
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `AUM: ₹${formatNumber(Math.round(ctx.parsed.x))} Cr`
                    }
                }
            },
            animation: { duration: 800 }
        }
    });
}

function updateRiskDistChart() {
    destroyChart('riskDist');
    const riskOrder = ['Low', 'Low to Moderate', 'Moderate', 'Moderately High', 'High', 'Very High'];
    const riskColors = ['#10b981', '#14b8a6', '#f59e0b', '#f97316', '#f43f5e', '#dc2626'];
    const counts = {};
    riskOrder.forEach(r => counts[r] = 0);
    FILTERED_FUNDS.forEach(f => {
        if (counts.hasOwnProperty(f['Risk Level'])) counts[f['Risk Level']]++;
    });

    const labels = riskOrder.filter(r => counts[r] > 0);
    const data = labels.map(r => counts[r]);
    const colors = labels.map(r => riskColors[riskOrder.indexOf(r)]);

    const ctx = document.getElementById('chartRiskDist').getContext('2d');
    CHARTS.riskDist = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.map(c => c + '66'),
                borderColor: colors,
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 }, padding: 10, boxWidth: 12, borderRadius: 3, useBorderRadius: true }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                }
            },
            scales: {
                r: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { display: false },
                }
            },
            animation: { duration: 800 }
        }
    });
}

// ── INSIGHTS ────────────────────────────────────────────────
function updateInsights() {
    const funds = FILTERED_FUNDS;
    const n = funds.length;
    if (!n) {
        document.getElementById('insightsGrid').innerHTML =
            '<div class="insight-card"><div class="insight-emoji">🔍</div><div class="insight-content"><h4>No Data</h4><p>Try adjusting your filters to see results.</p></div></div>';
        return;
    }

    const avgReturn = (funds.reduce((s, f) => s + f['Return 3Y (%)'], 0) / n).toFixed(1);
    const avgExpense = (funds.reduce((s, f) => s + f['Expense Ratio (%)'], 0) / n).toFixed(2);
    const topFund = funds.reduce((best, f) => f['Return 3Y (%)'] > best['Return 3Y (%)'] ? f : best, funds[0]);
    const lowExpFund = funds.reduce((best, f) => f['Expense Ratio (%)'] < best['Expense Ratio (%)'] ? f : best, funds[0]);
    const highAUM = funds.reduce((best, f) => f['AUM (Cr)'] > best['AUM (Cr)'] ? f : best, funds[0]);

    const fundTypes = {};
    funds.forEach(f => fundTypes[f['Fund Type']] = (fundTypes[f['Fund Type']] || 0) + 1);
    const dominantType = Object.entries(fundTypes).sort((a, b) => b[1] - a[1])[0];

    const lowRiskCount = funds.filter(f => f['Risk Level'] === 'Low' || f['Risk Level'] === 'Low to Moderate').length;

    const insights = [
        {
            emoji: '📈',
            title: 'Average 3-Year Return',
            text: `Across ${n} filtered funds, the average 3-year return stands at <strong>${avgReturn}%</strong>. This indicates ${avgReturn > 15 ? 'strong' : avgReturn > 10 ? 'moderate' : 'conservative'} growth potential.`
        },
        {
            emoji: '🏆',
            title: 'Top Performer',
            text: `<strong>${topFund['Scheme Name'].substring(0, 50)}...</strong> leads with a 3-year return of <strong>${topFund['Return 3Y (%)'].toFixed(1)}%</strong>.`
        },
        {
            emoji: '💰',
            title: 'Lowest Expense Ratio',
            text: `<strong>${lowExpFund['AMC Name']}</strong> offers the lowest expense at <strong>${lowExpFund['Expense Ratio (%)'].toFixed(2)}%</strong>, maximizing your net returns.`
        },
        {
            emoji: '🏦',
            title: 'Largest AUM',
            text: `<strong>${highAUM['AMC Name']}</strong> manages the highest AUM at <strong>₹${formatNumber(Math.round(highAUM['AUM (Cr)']))}</strong> Cr, showing strong investor confidence.`
        },
        {
            emoji: '📊',
            title: 'Dominant Fund Type',
            text: `<strong>${dominantType[0]}</strong> funds dominate with <strong>${dominantType[1]}</strong> schemes (${(dominantType[1] / n * 100).toFixed(0)}% of filtered results).`
        },
        {
            emoji: '🛡️',
            title: 'Low-Risk Options',
            text: `<strong>${lowRiskCount}</strong> funds (${(lowRiskCount / n * 100).toFixed(0)}%) are classified as Low or Low-to-Moderate risk, ideal for conservative investors.`
        },
    ];

    const grid = document.getElementById('insightsGrid');
    grid.innerHTML = insights.map(ins => `
        <div class="insight-card">
            <div class="insight-emoji">${ins.emoji}</div>
            <div class="insight-content">
                <h4>${ins.title}</h4>
                <p>${ins.text}</p>
            </div>
        </div>
    `).join('');
}

// ── TABLE ───────────────────────────────────────────────────
function updateTable() {
    const topFunds = FILTERED_FUNDS.slice(0, 30);
    const tbody = document.getElementById('top30Body');

    tbody.innerHTML = topFunds.map((f, i) => `
        <tr>
            <td>${i + 1}</td>
            <td title="${f['Scheme Name']}">${f['Scheme Name']}</td>
            <td>${f['AMC Name'].replace(' Mutual Fund', '')}</td>
            <td>${f['Fund Type']}</td>
            <td>${f['Category']}</td>
            <td><span class="risk-badge ${getRiskClass(f['Risk Level'])}">${f['Risk Level']}</span></td>
            <td><span class="rating-stars">${'★'.repeat(f['Fund Rating'])}${'☆'.repeat(5 - f['Fund Rating'])}</span></td>
            <td style="color: ${f['Return 3Y (%)'] > 20 ? '#34d399' : f['Return 3Y (%)'] > 10 ? '#fbbf24' : '#fb7185'}; font-weight: 600;">
                ${f['Return 3Y (%)'].toFixed(1)}%
            </td>
            <td>${f['Expense Ratio (%)'].toFixed(2)}%</td>
            <td>₹${formatNumber(Math.round(f['AUM (Cr)']))}</td>
            <td><span class="score-badge ${f.Score > 70 ? 'score-high' : f.Score > 40 ? 'score-mid' : 'score-low'}">${f.Score.toFixed(0)}</span></td>
        </tr>
    `).join('');
}

function getRiskClass(risk) {
    const map = {
        'Low': 'risk-low',
        'Low to Moderate': 'risk-low-mod',
        'Moderate': 'risk-moderate',
        'Moderately High': 'risk-mod-high',
        'High': 'risk-high',
        'Very High': 'risk-very-high',
    };
    return map[risk] || '';
}

// ── TABLE SORTING ───────────────────────────────────────────
let currentSort = { key: 'Score', dir: 'desc' };

function sortTable(th) {
    const key = th.dataset.sort;
    const dir = (currentSort.key === key && currentSort.dir === 'desc') ? 'asc' : 'desc';
    currentSort = { key, dir };

    // Update header classes
    document.querySelectorAll('.data-table thead th').forEach(h => {
        h.classList.remove('sort-asc', 'sort-desc');
    });
    th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');

    // Sort
    FILTERED_FUNDS.sort((a, b) => {
        let va = a[key], vb = b[key];
        if (typeof va === 'string') {
            return dir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
        }
        return dir === 'asc' ? va - vb : vb - va;
    });

    updateTable();
}

// ── UTILITY ─────────────────────────────────────────────────
function groupBy(data, key, valueKey, agg) {
    const groups = {};
    data.forEach(item => {
        const k = item[key];
        if (!groups[k]) groups[k] = [];
        groups[k].push(item[valueKey]);
    });

    const result = {};
    for (const [k, vals] of Object.entries(groups)) {
        if (agg === 'avg') {
            result[k] = parseFloat((vals.reduce((s, v) => s + v, 0) / vals.length).toFixed(2));
        } else if (agg === 'sum') {
            result[k] = parseFloat(vals.reduce((s, v) => s + v, 0).toFixed(2));
        } else if (agg === 'count') {
            result[k] = vals.length;
        }
    }
    return result;
}

function createGradientBars(ctx, count, color1, color2) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const ratio = count > 1 ? i / (count - 1) : 0;
        colors.push(interpolateColor(color1, color2, ratio));
    }
    return colors;
}

function interpolateColor(hex1, hex2, ratio) {
    const r1 = parseInt(hex1.slice(1, 3), 16);
    const g1 = parseInt(hex1.slice(3, 5), 16);
    const b1 = parseInt(hex1.slice(5, 7), 16);
    const r2 = parseInt(hex2.slice(1, 3), 16);
    const g2 = parseInt(hex2.slice(3, 5), 16);
    const b2 = parseInt(hex2.slice(5, 7), 16);
    const r = Math.round(r1 + (r2 - r1) * ratio);
    const g = Math.round(g1 + (g2 - g1) * ratio);
    const b = Math.round(b1 + (b2 - b1) * ratio);
    return `rgb(${r}, ${g}, ${b})`;
}
