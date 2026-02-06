"""Tests for trading agents."""
import pytest
import asyncio
from src.agents import (
    MarketDataAgent,
    AnalysisAgent,
    SignalAgent,
    RiskAgent,
    ExecutionAgent,
    PortfolioAgent,
)
from src.core.message_bus import message_bus
from src.core.events import EventType


@pytest.fixture
async def setup_message_bus():
    """Setup message bus for tests."""
    await message_bus.start()
    yield
    await message_bus.stop()


@pytest.mark.asyncio
async def test_market_data_agent_initialization():
    """Test market data agent initialization."""
    agent = MarketDataAgent(symbols=["AAPL", "GOOGL"])
    assert agent.name == "MarketDataAgent"
    assert len(agent.symbols) == 2
    assert not agent.running


@pytest.mark.asyncio
async def test_analysis_agent_initialization():
    """Test analysis agent initialization."""
    agent = AnalysisAgent()
    assert agent.name == "AnalysisAgent"
    assert agent.max_history_length == 200


@pytest.mark.asyncio
async def test_signal_agent_initialization():
    """Test signal agent initialization."""
    agent = SignalAgent()
    assert agent.name == "SignalAgent"
    assert len(agent.latest_analysis) == 0


@pytest.mark.asyncio
async def test_risk_agent_initialization():
    """Test risk agent initialization."""
    agent = RiskAgent(initial_capital=100000)
    assert agent.name == "RiskAgent"
    assert agent.capital == 100000
    assert agent.max_position_size > 0


@pytest.mark.asyncio
async def test_execution_agent_initialization():
    """Test execution agent initialization."""
    agent = ExecutionAgent()
    assert agent.name == "ExecutionAgent"
    assert agent.paper_trading is True


@pytest.mark.asyncio
async def test_portfolio_agent_initialization():
    """Test portfolio agent initialization."""
    agent = PortfolioAgent(initial_capital=100000)
    assert agent.name == "PortfolioAgent"
    assert agent.cash == 100000
    assert agent.total_value == 100000


@pytest.mark.asyncio
async def test_agent_start_stop(setup_message_bus):
    """Test agent start and stop."""
    agent = AnalysisAgent()
    
    await agent.start()
    assert agent.running is True
    
    await asyncio.sleep(0.5)
    
    await agent.stop()
    assert agent.running is False


@pytest.mark.asyncio
async def test_portfolio_agent_buy_order(setup_message_bus):
    """Test portfolio agent handling buy order."""
    agent = PortfolioAgent(initial_capital=100000)
    await agent.initialize()
    await agent.subscribe_to_events()
    
    # Simulate order filled event
    from src.core.events import Event
    event = Event(
        event_type=EventType.ORDER_FILLED,
        source_agent="TestAgent",
        data={
            "symbol": "AAPL",
            "side": "BUY",
            "quantity": 10,
            "price": 150.0
        }
    )
    
    await agent.handle_event(event)
    
    assert "AAPL" in agent.positions
    assert agent.positions["AAPL"]["quantity"] == 10
    assert agent.cash < 100000  # Cash should decrease


@pytest.mark.asyncio
async def test_risk_agent_position_sizing():
    """Test risk agent position sizing calculation."""
    agent = RiskAgent(initial_capital=100000)
    
    position_size = await agent._calculate_position_size(
        symbol="AAPL",
        price=150.0,
        stop_loss=145.0
    )
    
    assert position_size > 0
    assert isinstance(position_size, float)
