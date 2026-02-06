// Finlytics Trading System - Frontend Application
// Demo Mode - Simulated Data

// Configuration
const CONFIG = {
    updateInterval: 3000, // 3 seconds
    demoMode: true,
    symbols: ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']
};

// State Management
const state = {
    portfolio: {
        totalValue: 100000,
        cash: 100000,
        pnl: 0,
        positions: 0
    },
    trades: [],
    signals: [],
    agents: [
        { name: 'Market Data Agent', status: 'active', description: 'Streaming real-time data' },
        { name: 'Analysis Agent', status: 'active', description: 'Running technical analysis' },
        { name: 'Signal Agent', status: 'active', description: 'Generating signals' },
        { name: 'Risk Agent', status: 'active', description: 'Monitoring risk levels' },
        { name: 'Execution Agent', status: 'idle', description: 'Ready for orders' },
        { name: 'Portfolio Agent', status: 'active', description: 'Tracking portfolio' }
    ],
    marketData: {}
};

// Initialize Application
function init() {
    console.log('🚀 Finlytics Trading System Initializing...');
    updateSystemStatus('active');
    renderAgents();
    generateDemoData();
    startDataUpdates();
    console.log('✅ System Ready');
}

// Update System Status
function updateSystemStatus(status) {
    const statusDot = document.getElementById('systemStatus');
    const statusText = document.getElementById('statusText');
    
    if (status === 'active') {
        statusDot.style.background = 'var(--success-color)';
        statusText.textContent = 'System Active';
    } else {
        statusDot.style.background = 'var(--danger-color)';
        statusText.textContent = 'System Offline';
    }
}

// Generate Demo Data
function generateDemoData() {
    // Generate market data
    CONFIG.symbols.forEach(symbol => {
        const basePrice = Math.random() * 500 + 100;
        state.marketData[symbol] = {
            symbol: symbol,
            price: basePrice,
            change: (Math.random() - 0.5) * 10,
            changePercent: (Math.random() - 0.5) * 5
        };
    });

    // Generate demo trades
    const tradeTypes = ['BUY', 'SELL'];
    const statuses = ['FILLED', 'FILLED', 'FILLED', 'PENDING'];
    
    for (let i = 0; i < 5; i++) {
        const symbol = CONFIG.symbols[Math.floor(Math.random() * CONFIG.symbols.length)];
        const type = tradeTypes[Math.floor(Math.random() * tradeTypes.length)];
        const quantity = Math.floor(Math.random() * 100) + 10;
        const price = state.marketData[symbol].price;
        const pnl = type === 'SELL' ? (Math.random() - 0.3) * 1000 : 0;
        
        state.trades.push({
            time: new Date(Date.now() - Math.random() * 3600000).toLocaleTimeString(),
            symbol: symbol,
            type: type,
            quantity: quantity,
            price: price.toFixed(2),
            pnl: pnl.toFixed(2),
            status: statuses[Math.floor(Math.random() * statuses.length)]
        });
    }

    // Generate demo signals
    const signalTypes = ['BUY', 'SELL'];
    const strategies = ['Momentum', 'Mean Reversion', 'Trend Following'];
    
    for (let i = 0; i < 3; i++) {
        const symbol = CONFIG.symbols[Math.floor(Math.random() * CONFIG.symbols.length)];
        const type = signalTypes[Math.floor(Math.random() * signalTypes.length)];
        const confidence = (Math.random() * 30 + 70).toFixed(1);
        
        state.signals.push({
            symbol: symbol,
            type: type,
            confidence: confidence,
            strategy: strategies[Math.floor(Math.random() * strategies.length)],
            price: state.marketData[symbol].price.toFixed(2)
        });
    }

    // Update portfolio
    state.portfolio.positions = Math.floor(Math.random() * 5) + 2;
    state.portfolio.totalValue = 100000 + (Math.random() - 0.3) * 5000;
    state.portfolio.cash = state.portfolio.totalValue * (0.3 + Math.random() * 0.4);
    state.portfolio.pnl = state.portfolio.totalValue - 100000;

    renderAll();
}

// Render All Components
function renderAll() {
    renderPortfolio();
    renderStats();
    renderTrades();
    renderSignals();
    renderMarketData();
}

// Render Portfolio
function renderPortfolio() {
    document.getElementById('totalValue').textContent = `$${state.portfolio.totalValue.toFixed(2).toLocaleString()}`;
    document.getElementById('cashAvailable').textContent = `$${state.portfolio.cash.toFixed(2).toLocaleString()}`;
    document.getElementById('totalPnL').textContent = `$${state.portfolio.pnl.toFixed(2).toLocaleString()}`;
    document.getElementById('activePositions').textContent = state.portfolio.positions;
    
    const changePercent = (state.portfolio.pnl / 100000 * 100).toFixed(2);
    const changeElement = document.getElementById('totalChange');
    changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent}%`;
    changeElement.className = `stat-change ${changePercent >= 0 ? 'positive' : 'negative'}`;
    
    const pnlChangeElement = document.getElementById('pnlChange');
    pnlChangeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent}%`;
    pnlChangeElement.className = `stat-change ${changePercent >= 0 ? 'positive' : 'negative'}`;
}

// Render Statistics
function renderStats() {
    const totalTrades = state.trades.length;
    const filledTrades = state.trades.filter(t => t.status === 'FILLED').length;
    const profitableTrades = state.trades.filter(t => parseFloat(t.pnl) > 0).length;
    const winRate = filledTrades > 0 ? (profitableTrades / filledTrades * 100).toFixed(1) : 0;
    const avgTradeSize = totalTrades > 0 ? 
        (state.trades.reduce((sum, t) => sum + (t.quantity * parseFloat(t.price)), 0) / totalTrades).toFixed(0) : 0;
    
    document.getElementById('totalTrades').textContent = totalTrades;
    document.getElementById('winRate').textContent = `${winRate}%`;
    document.getElementById('activeSignals').textContent = state.signals.length;
    document.getElementById('avgTradeSize').textContent = `$${avgTradeSize.toLocaleString()}`;
}

// Render Agents
function renderAgents() {
    const agentsGrid = document.getElementById('agentsGrid');
    agentsGrid.innerHTML = state.agents.map(agent => `
        <div class="agent-card">
            <div class="agent-info">
                <h3>${agent.name}</h3>
                <p>${agent.description}</p>
            </div>
            <span class="agent-status-badge ${agent.status}">${agent.status}</span>
        </div>
    `).join('');
}

// Render Trades
function renderTrades() {
    const tradesBody = document.getElementById('tradesBody');
    
    if (state.trades.length === 0) {
        tradesBody.innerHTML = '<tr><td colspan="7" class="no-data">No trades yet. System is in demo mode.</td></tr>';
        return;
    }
    
    tradesBody.innerHTML = state.trades.map(trade => `
        <tr>
            <td>${trade.time}</td>
            <td><strong>${trade.symbol}</strong></td>
            <td><span class="badge ${trade.type.toLowerCase()}">${trade.type}</span></td>
            <td>${trade.quantity}</td>
            <td>$${trade.price}</td>
            <td class="${parseFloat(trade.pnl) >= 0 ? 'positive' : 'negative'}">
                ${parseFloat(trade.pnl) >= 0 ? '+' : ''}$${trade.pnl}
            </td>
            <td>${trade.status}</td>
        </tr>
    `).join('');
}

// Render Signals
function renderSignals() {
    const signalsContainer = document.getElementById('signalsContainer');
    
    if (state.signals.length === 0) {
        signalsContainer.innerHTML = '<p class="no-data">No active signals. Monitoring markets...</p>';
        return;
    }
    
    signalsContainer.innerHTML = state.signals.map(signal => `
        <div class="signal-card ${signal.type.toLowerCase()}">
            <div>
                <h3>${signal.symbol} - ${signal.type}</h3>
                <p>Strategy: ${signal.strategy} | Price: $${signal.price}</p>
            </div>
            <div>
                <strong>Confidence: ${signal.confidence}%</strong>
            </div>
        </div>
    `).join('');
}

// Render Market Data
function renderMarketData() {
    const marketGrid = document.getElementById('marketGrid');
    
    marketGrid.innerHTML = Object.values(state.marketData).map(data => `
        <div class="market-item">
            <div class="market-symbol">${data.symbol}</div>
            <div class="market-price">$${data.price.toFixed(2)}</div>
            <div class="market-change ${data.changePercent >= 0 ? 'positive' : 'negative'}">
                ${data.changePercent >= 0 ? '+' : ''}${data.changePercent.toFixed(2)}%
            </div>
        </div>
    `).join('');
}

// Update Market Data (Simulated)
function updateMarketData() {
    Object.keys(state.marketData).forEach(symbol => {
        const data = state.marketData[symbol];
        const change = (Math.random() - 0.5) * 2;
        data.price += change;
        data.change += change;
        data.changePercent = (data.change / (data.price - data.change)) * 100;
    });
    
    // Randomly update portfolio
    if (Math.random() > 0.7) {
        state.portfolio.totalValue += (Math.random() - 0.5) * 500;
        state.portfolio.pnl = state.portfolio.totalValue - 100000;
    }
    
    renderAll();
}

// Start Data Updates
function startDataUpdates() {
    setInterval(() => {
        updateMarketData();
    }, CONFIG.updateInterval);
}

// Refresh Data
function refreshData() {
    console.log('🔄 Refreshing data...');
    generateDemoData();
    showNotification('Data refreshed successfully!', 'success');
}

// View Logs
function viewLogs() {
    const logs = [
        '[INFO] System started successfully',
        '[INFO] Market Data Agent: Connected to data stream',
        '[INFO] Analysis Agent: Running technical analysis on 6 symbols',
        '[INFO] Signal Agent: Generated 3 new signals',
        '[INFO] Risk Agent: All positions within risk limits',
        '[INFO] Portfolio Agent: Portfolio value updated'
    ];
    
    alert('📋 System Logs:\n\n' + logs.join('\n'));
}

// Download Report
function downloadReport() {
    const report = {
        timestamp: new Date().toISOString(),
        portfolio: state.portfolio,
        trades: state.trades,
        signals: state.signals,
        marketData: state.marketData
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `finlytics-report-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification('Report downloaded successfully!', 'success');
}

// Show Documentation
function showDocumentation() {
    document.getElementById('docModal').style.display = 'block';
}

// Close Modal
function closeModal() {
    document.getElementById('docModal').style.display = 'none';
}

// Show Notification
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // You can implement a toast notification here
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('docModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Export functions for global access
window.refreshData = refreshData;
window.viewLogs = viewLogs;
window.downloadReport = downloadReport;
window.showDocumentation = showDocumentation;
window.closeModal = closeModal;
