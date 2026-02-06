"""Orchestrator - Manages all agents and coordinates the trading system."""
import asyncio
from typing import List, Dict
from src.agents.base_agent import BaseAgent
from src.core.message_bus import message_bus
from src.core.logger import log


class Orchestrator:
    """Central orchestrator for managing all trading agents."""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.running = False
        
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator."""
        self.agents.append(agent)
        log.info(f"Registered agent: {agent.name}")
    
    def register_agents(self, agents: List[BaseAgent]):
        """Register multiple agents."""
        for agent in agents:
            self.register_agent(agent)
    
    async def start(self):
        """Start all agents and the message bus."""
        if self.running:
            log.warning("Orchestrator is already running")
            return
        
        self.running = True
        log.info("Starting Orchestrator")
        
        # Start message bus
        await message_bus.start()
        
        # Start all agents
        start_tasks = []
        for agent in self.agents:
            start_tasks.append(agent.start())
        
        await asyncio.gather(*start_tasks)
        
        log.info(f"All {len(self.agents)} agents started successfully")
    
    async def stop(self):
        """Stop all agents and the message bus."""
        if not self.running:
            return
        
        self.running = False
        log.info("Stopping Orchestrator")
        
        # Stop all agents
        stop_tasks = []
        for agent in self.agents:
            stop_tasks.append(agent.stop())
        
        await asyncio.gather(*stop_tasks, return_exceptions=True)
        
        # Stop message bus
        await message_bus.stop()
        
        log.info("All agents stopped")
    
    async def run(self, duration: int = None):
        """Run the orchestrator for a specified duration or indefinitely."""
        await self.start()
        
        try:
            if duration:
                log.info(f"Running for {duration} seconds")
                await asyncio.sleep(duration)
            else:
                log.info("Running indefinitely (Ctrl+C to stop)")
                while self.running:
                    await asyncio.sleep(1)
        except KeyboardInterrupt:
            log.info("Received interrupt signal")
        finally:
            await self.stop()
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents."""
        return {
            agent.name: {
                "running": agent.running,
                "type": agent.__class__.__name__
            }
            for agent in self.agents
        }
    
    async def restart_agent(self, agent_name: str):
        """Restart a specific agent."""
        for agent in self.agents:
            if agent.name == agent_name:
                log.info(f"Restarting agent: {agent_name}")
                await agent.stop()
                await asyncio.sleep(1)
                await agent.start()
                return True
        
        log.warning(f"Agent not found: {agent_name}")
        return False
    
    def __repr__(self):
        return f"<Orchestrator agents={len(self.agents)} running={self.running}>"
