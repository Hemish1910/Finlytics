"""
Finlytics Trading System - Web API
FastAPI application for real-time trading dashboard
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import with error handling for deployment
try:
    from src.core.orchestrator import TradingOrchestrator
    from src.core.config import Config
    from src.models.database import init_db, get_session, Trade, Position, Signal, AgentStatus
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Import warning: {e}")
    IMPORTS_AVAILABLE = False
    # Mock classes for deployment
    class Trade: pass
    class Position: pass
    class Signal: pass
    class AgentStatus: pass
    def init_db(): pass
    def get_session(): return None

app = FastAPI(title="Finlytics Trading System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = None
active_connections: List[WebSocket] = []

@app.on_event("startup")
async def startup_event():
    """Initialize the trading system on startup"""
    global orchestrator
    
    if IMPORTS_AVAILABLE:
        try:
            # Initialize database
            init_db()
            
            # Create orchestrator (but don't start background tasks in serverless)
            config = Config()
            orchestrator = TradingOrchestrator(config)
            
            print("Trading system initialized (serverless mode)")
        except Exception as e:
            print(f"Startup error: {e}")
            # Continue with demo mode
    else:
        print("Running in demo mode - imports not available")

def get_or_create_orchestrator():
    """Get or create orchestrator instance for serverless"""
    global orchestrator
    if orchestrator is None and IMPORTS_AVAILABLE:
        try:
            init_db()
            config = Config()
            orchestrator = TradingOrchestrator(config)
        except Exception as e:
            print(f"Error creating orchestrator: {e}")
    return orchestrator

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the main dashboard HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Finlytics - Real-Time Trading System</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }
            .header h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            .status-badge {
                display: inline-block;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 15px;
                font-size: 0.9em;
            }
            .status-running { background: #10b981; color: white; }
            .status-stopped { background: #ef4444; color: white; }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .card h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3em;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .metric {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }
            .metric:last-child { border-bottom: none; }
            .metric-label {
                color: #666;
                font-weight: 500;
            }
            .metric-value {
                font-weight: bold;
                color: #333;
            }
            .positive { color: #10b981; }
            .negative { color: #ef4444; }
            .agent-list {
                list-style: none;
            }
            .agent-item {
                padding: 12px;
                margin: 8px 0;
                background: #f8f9fa;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .agent-status {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 10px;
            }
            .agent-active { background: #10b981; }
            .agent-inactive { background: #ef4444; }
            .table-container {
                overflow-x: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            th {
                background: #f8f9fa;
                font-weight: 600;
                color: #667eea;
            }
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                font-size: 1em;
                margin: 5px;
                transition: all 0.3s;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            .btn-danger {
                background: #ef4444;
                color: white;
            }
            .btn-danger:hover {
                background: #dc2626;
            }
            .controls {
                text-align: center;
                margin-top: 20px;
            }
            .loading {
                text-align: center;
                padding: 20px;
                color: #666;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .pulse { animation: pulse 2s infinite; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Finlytics Trading System</h1>
                <p>Real-Time Multi-Agent Trading Platform</p>
                <span id="systemStatus" class="status-badge status-running">● SYSTEM RUNNING</span>
            </div>

            <div class="grid">
                <div class="card">
                    <h2>📊 Portfolio Overview</h2>
                    <div class="metric">
                        <span class="metric-label">Total Value</span>
                        <span class="metric-value" id="portfolioValue">$100,000.00</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Cash Available</span>
                        <span class="metric-value" id="cashAvailable">$100,000.00</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Total P&L</span>
                        <span class="metric-value positive" id="totalPnL">$0.00</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Open Positions</span>
                        <span class="metric-value" id="openPositions">0</span>
                    </div>
                </div>

                <div class="card">
                    <h2>📈 Trading Statistics</h2>
                    <div class="metric">
                        <span class="metric-label">Total Trades</span>
                        <span class="metric-value" id="totalTrades">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Win Rate</span>
                        <span class="metric-value" id="winRate">0%</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Active Signals</span>
                        <span class="metric-value" id="activeSignals">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Avg Trade Size</span>
                        <span class="metric-value" id="avgTradeSize">$0.00</span>
                    </div>
                </div>

                <div class="card">
                    <h2>🤖 Agent Status</h2>
                    <ul class="agent-list" id="agentList">
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Market Data Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Analysis Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Signal Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Risk Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Execution Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                        <li class="agent-item">
                            <span><span class="agent-status agent-active"></span>Portfolio Agent</span>
                            <span class="metric-value">Active</span>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="card">
                <h2>📋 Recent Trades</h2>
                <div class="table-container">
                    <table id="tradesTable">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Symbol</th>
                                <th>Side</th>
                                <th>Quantity</th>
                                <th>Price</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="tradesBody">
                            <tr>
                                <td colspan="6" class="loading pulse">Waiting for trades...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>🎯 Active Signals</h2>
                <div class="table-container">
                    <table id="signalsTable">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Symbol</th>
                                <th>Signal</th>
                                <th>Confidence</th>
                                <th>Strategy</th>
                            </tr>
                        </thead>
                        <tbody id="signalsBody">
                            <tr>
                                <td colspan="5" class="loading pulse">Waiting for signals...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card controls">
                <h2>⚙️ System Controls</h2>
                <button class="btn btn-primary" onclick="refreshData()">🔄 Refresh Data</button>
                <button class="btn btn-primary" onclick="viewLogs()">📝 View Logs</button>
                <button class="btn btn-primary" onclick="downloadReport()">📊 Download Report</button>
            </div>
        </div>

        <script>
            let ws = null;
            
            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
                
                ws.onopen = () => {
                    console.log('WebSocket connected');
                    document.getElementById('systemStatus').textContent = '● SYSTEM RUNNING';
                    document.getElementById('systemStatus').className = 'status-badge status-running';
                };
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    updateDashboard(data);
                };
                
                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
                
                ws.onclose = () => {
                    console.log('WebSocket disconnected');
                    document.getElementById('systemStatus').textContent = '● RECONNECTING...';
                    document.getElementById('systemStatus').className = 'status-badge status-stopped';
                    setTimeout(connectWebSocket, 3000);
                };
            }
            
            function updateDashboard(data) {
                if (data.type === 'portfolio_update') {
                    document.getElementById('portfolioValue').textContent = `$${data.total_value.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
                    document.getElementById('cashAvailable').textContent = `$${data.cash.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
                    const pnl = data.total_pnl;
                    const pnlElement = document.getElementById('totalPnL');
                    pnlElement.textContent = `$${Math.abs(pnl).toLocaleString('en-US', {minimumFractionDigits: 2})}`;
                    pnlElement.className = pnl >= 0 ? 'metric-value positive' : 'metric-value negative';
                }
                
                if (data.type === 'trade_update') {
                    addTradeToTable(data.trade);
                }
                
                if (data.type === 'signal_update') {
                    addSignalToTable(data.signal);
                }
            }
            
            function addTradeToTable(trade) {
                const tbody = document.getElementById('tradesBody');
                if (tbody.querySelector('.loading')) {
                    tbody.innerHTML = '';
                }
                
                const row = tbody.insertRow(0);
                row.innerHTML = `
                    <td>${new Date(trade.timestamp).toLocaleTimeString()}</td>
                    <td><strong>${trade.symbol}</strong></td>
                    <td><span class="${trade.side === 'BUY' ? 'positive' : 'negative'}">${trade.side}</span></td>
                    <td>${trade.quantity}</td>
                    <td>$${trade.price.toFixed(2)}</td>
                    <td>${trade.status}</td>
                `;
                
                // Keep only last 10 trades
                while (tbody.rows.length > 10) {
                    tbody.deleteRow(tbody.rows.length - 1);
                }
            }
            
            function addSignalToTable(signal) {
                const tbody = document.getElementById('signalsBody');
                if (tbody.querySelector('.loading')) {
                    tbody.innerHTML = '';
                }
                
                const row = tbody.insertRow(0);
                row.innerHTML = `
                    <td>${new Date(signal.timestamp).toLocaleTimeString()}</td>
                    <td><strong>${signal.symbol}</strong></td>
                    <td><span class="${signal.signal_type === 'BUY' ? 'positive' : 'negative'}">${signal.signal_type}</span></td>
                    <td>${(signal.confidence * 100).toFixed(1)}%</td>
                    <td>${signal.strategy}</td>
                `;
                
                // Keep only last 10 signals
                while (tbody.rows.length > 10) {
                    tbody.deleteRow(tbody.rows.length - 1);
                }
            }
            
            async function refreshData() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    document.getElementById('totalTrades').textContent = data.total_trades || 0;
                    document.getElementById('openPositions').textContent = data.open_positions || 0;
                    document.getElementById('activeSignals').textContent = data.active_signals || 0;
                    
                    console.log('Data refreshed');
                } catch (error) {
                    console.error('Error refreshing data:', error);
                }
            }
            
            function viewLogs() {
                window.open('/api/logs', '_blank');
            }
            
            function downloadReport() {
                window.location.href = '/api/report';
            }
            
            // Initialize
            connectWebSocket();
            setInterval(refreshData, 5000);
            refreshData();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    if not IMPORTS_AVAILABLE:
        # Demo mode
        return {
            "status": "demo",
            "total_trades": 0,
            "open_positions": 0,
            "active_signals": 0,
            "agents": [
                {"name": "Market Data Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
                {"name": "Analysis Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
                {"name": "Signal Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
                {"name": "Risk Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
                {"name": "Execution Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
                {"name": "Portfolio Agent", "status": "active", "last_heartbeat": datetime.now().isoformat()},
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    session = get_session()
    
    try:
        total_trades = session.query(Trade).count()
        open_positions = session.query(Position).filter(Position.quantity > 0).count()
        active_signals = session.query(Signal).filter(Signal.timestamp >= datetime.now().replace(hour=0, minute=0, second=0)).count()
        
        agents = session.query(AgentStatus).all()
        agent_status = [
            {
                "name": agent.agent_name,
                "status": agent.status,
                "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None
            }
            for agent in agents
        ]
        
        return {
            "status": "running",
            "total_trades": total_trades,
            "open_positions": open_positions,
            "active_signals": active_signals,
            "agents": agent_status,
            "timestamp": datetime.now().isoformat()
        }
    finally:
        if session:
            session.close()

@app.get("/api/portfolio")
async def get_portfolio():
    """Get portfolio information"""
    if not IMPORTS_AVAILABLE:
        # Demo mode
        return {
            "cash": 100000.0,
            "positions": [],
            "total_value": 100000.0,
            "total_pnl": 0.0
        }
    
    session = get_session()
    
    try:
        positions = session.query(Position).filter(Position.quantity > 0).all()
        
        portfolio_data = {
            "cash": 100000.0,  # Default starting cash
            "positions": [
                {
                    "symbol": pos.symbol,
                    "quantity": pos.quantity,
                    "avg_price": pos.avg_price,
                    "current_price": pos.current_price,
                    "unrealized_pnl": pos.unrealized_pnl,
                    "realized_pnl": pos.realized_pnl
                }
                for pos in positions
            ],
            "total_value": 100000.0 + sum(pos.unrealized_pnl for pos in positions),
            "total_pnl": sum(pos.unrealized_pnl + pos.realized_pnl for pos in positions)
        }
        
        return portfolio_data
    finally:
        if session:
            session.close()

@app.get("/api/trades")
async def get_trades(limit: int = 50):
    """Get recent trades"""
    if not IMPORTS_AVAILABLE:
        # Demo mode
        return {"trades": []}
    
    session = get_session()
    
    try:
        trades = session.query(Trade).order_by(Trade.timestamp.desc()).limit(limit).all()
        
        return {
            "trades": [
                {
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "side": trade.side,
                    "quantity": trade.quantity,
                    "price": trade.price,
                    "status": trade.status,
                    "timestamp": trade.timestamp.isoformat()
                }
                for trade in trades
            ]
        }
    finally:
        if session:
            session.close()

@app.get("/api/signals")
async def get_signals(limit: int = 50):
    """Get recent signals"""
    if not IMPORTS_AVAILABLE:
        # Demo mode
        return {"signals": []}
    
    session = get_session()
    
    try:
        signals = session.query(Signal).order_by(Signal.timestamp.desc()).limit(limit).all()
        
        return {
            "signals": [
                {
                    "id": signal.id,
                    "symbol": signal.symbol,
                    "signal_type": signal.signal_type,
                    "confidence": signal.confidence,
                    "strategy": signal.strategy,
                    "timestamp": signal.timestamp.isoformat()
                }
                for signal in signals
            ]
        }
    finally:
        if session:
            session.close()

@app.get("/api/logs")
async def get_logs():
    """Get system logs"""
    try:
        log_file = "/vercel/sandbox/logs/trading_system.log"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.readlines()[-100:]  # Last 100 lines
            return {"logs": logs}
        else:
            return {"logs": ["No logs available yet"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/report")
async def download_report():
    """Generate and download trading report"""
    if not IMPORTS_AVAILABLE:
        # Demo mode
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_trades": 0,
                "total_signals": 0
            },
            "trades": []
        }
        return JSONResponse(content=report)
    
    session = get_session()
    
    try:
        trades = session.query(Trade).all()
        signals = session.query(Signal).all()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_trades": len(trades),
                "total_signals": len(signals)
            },
            "trades": [
                {
                    "symbol": t.symbol,
                    "side": t.side,
                    "quantity": t.quantity,
                    "price": t.price,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in trades
            ]
        }
        
        return JSONResponse(content=report)
    finally:
        if session:
            session.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send periodic updates
            await asyncio.sleep(2)
            
            if not IMPORTS_AVAILABLE:
                # Demo mode
                update = {
                    "type": "portfolio_update",
                    "total_value": 100000.0,
                    "cash": 100000.0,
                    "total_pnl": 0.0,
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(update))
            else:
                # Get latest portfolio data
                session = get_session()
                try:
                    positions = session.query(Position).filter(Position.quantity > 0).all()
                    total_pnl = sum(pos.unrealized_pnl + pos.realized_pnl for pos in positions)
                    
                    update = {
                        "type": "portfolio_update",
                        "total_value": 100000.0 + sum(pos.unrealized_pnl for pos in positions),
                        "cash": 100000.0,
                        "total_pnl": total_pnl,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    await websocket.send_text(json.dumps(update))
                finally:
                    if session:
                        session.close()
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Vercel serverless function handler
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
