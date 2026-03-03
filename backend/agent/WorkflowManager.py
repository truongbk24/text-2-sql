from langgraph.graph import StateGraph, END
from agent.State import AgentState
from agent.SQLAgent import SQLAgent

class WorkflowManager:
    def __init__(self):
        self.sql_agent = SQLAgent()
        
    def create_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(AgentState)

        # Add nodes to the graph
        workflow.add_node("parse_question", self.sql_agent.parsed_question)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql)
        workflow.add_node("validate_and_fix_sql", self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.sql_agent.execute_sql)
        workflow.add_node("end_max_iterations", self.sql_agent.end_max_iterations)
        workflow.add_node("format_results", self.sql_agent.format_results)

        
        # Define edges
        workflow.add_edge("parse_question", "generate_sql")
        workflow.add_edge("generate_sql", "execute_sql")
        workflow.add_conditional_edges(
            "execute_sql",
            self.execute_sql_router,
            {
                "validate_and_fix_sql": "validate_and_fix_sql",
                "format_results": "format_results",
            },
        )
        workflow.add_conditional_edges(
            "validate_and_fix_sql",
            self.check_attempts_router,
            {
                "execute_sql": "execute_sql",
                "max_iterations": "end_max_iterations",
            },
        )
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("format_results", END)
        workflow.add_edge("end_max_iterations", END)
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
        
    def execute_sql_router(self, state: AgentState):
        sql_error = state.get("sql_issues")
        if sql_error:
            return "validate_and_fix_sql"
        else:
            return "format_results"
        
    def check_attempts_router(self,state: AgentState):
        if state["attempts"] < 3:
            return "execute_sql"
        else:
            return "end_max_iterations"