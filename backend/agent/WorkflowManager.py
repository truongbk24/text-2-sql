from langgraph.graph import StateGraph, END
from agent.State import InputState, OutputState
from agent.SQLAgent import SQLAgent

class WorkflowManager:
    def __init__(self):
        self.sql_agent = SQLAgent()
        
    def create_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(OutputState)

        # Add nodes to the graph
        workflow.add_node("parse_question", self.sql_agent.parsed_question)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql)
        workflow.add_node("validate_and_fix_sql", self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.sql_agent.execute_sql)
        workflow.add_node("format_results", self.sql_agent.format_results)

        
        # Define edges
        workflow.add_edge("parse_question", "generate_sql")
        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("format_results", END)
        workflow.set_entry_point("parse_question")

        return workflow
    
    def returnGraph(self):
        """Return the configured workflow graph."""
        return self.create_workflow().compile()
    
    def run_sql_agent(self, question: str) -> dict:
        """Run the SQL agent workflow with the given question."""
        app = self.create_workflow().compile()
        result = app.invoke({"question": question})
        return {
            "answer": result['answer']
        }