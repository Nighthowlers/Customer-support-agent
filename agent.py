# ruff: noqa
import os
from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
from google.adk.workflow import Workflow, START, Edge, FunctionNode
from google.adk.agents.context import Context

# Load environment variables
load_dotenv()

# Map GOOGLE_API_KEY to GEMINI_API_KEY if needed
if "GOOGLE_API_KEY" in os.environ and "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

if os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    try:
        import google.auth
        _, project_id = google.auth.default()
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    except Exception:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


# Define the Classifier Agent
classifier_agent = Agent(
    name="classifier_agent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "You are a routing classifier for a shipping company's customer support. "
        "Analyze the user query. "
        "If the query is related to shipping (e.g. shipping rates, tracking packages, delivery issues, return policies, return shipping, or delivery times), reply exactly with 'shipping'. "
        "If it is unrelated to shipping (e.g. general knowledge, greetings, weather, coding, or math), reply exactly with 'unrelated'."
    ),
)

# Define the Shipping FAQ Agent
faq_agent = Agent(
    name="faq_agent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "You are a helpful customer support representative for a shipping company. "
        "Answer the user's shipping-related questions (e.g. shipping rates, tracking, delivery, returns) "
        "politely, accurately, and professionally based on standard shipping policies. "
        "Ensure you explicitly address the specific concerns mentioned in the query. "
        "Make shipping rates responses extra playful, enthusiastic, and loaded with fun emojis! "
        "Always highlight that orders over $50 qualify for FREE shipping! 🚚🎉✨"
    ),
)


# Define the Decline Agent
decline_agent = Agent(
    name="decline_agent",
    model=Gemini(model="gemini-2.5-flash"),
    instruction=(
        "You are a customer support representative for a shipping company. "
        "The user has asked a question that is unrelated to shipping. "
        "Politely decline to answer the question, explaining that you can only assist with shipping-related topics "
        "(such as rates, tracking, delivery, or returns)."
    ),
)


# Define the classify and route node function
async def classify_and_route(ctx: Context, node_input: str) -> str:
    """Classifies the query and sets the route, passing the original query down."""
    # Programmatically run the classifier agent to get the classification
    classification_result = await ctx.run_node(classifier_agent, node_input)
    
    # Check the result to set the routing path
    result_clean = str(classification_result).strip().lower()
    if "shipping" in result_clean:
        ctx.route = "shipping"
    else:
        ctx.route = "unrelated"
        
    # Return the original user query so downstream nodes receive it as node_input
    return node_input


# Instantiate the FunctionNodes
classify_and_route_node = FunctionNode(func=classify_and_route, name="classify_and_route", rerun_on_resume=True)


# Define the main workflow graph
root_agent = Workflow(
    name="root_agent",
    edges=[
        Edge(from_node=START, to_node=classify_and_route_node),
        Edge(from_node=classify_and_route_node, to_node=faq_agent, route="shipping"),
        Edge(from_node=classify_and_route_node, to_node=decline_agent, route="unrelated"),
    ],
)

