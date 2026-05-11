from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime
from database import SessionLocal, Interaction
from langgraph.graph import StateGraph
import os

# =========================
# LOAD ENV
# =========================
load_dotenv()

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# LANGGRAPH STATE
# =========================
class State(dict):
    pass


# =========================
# AI EXTRACTION LOGIC
# =========================
def extract_data(user_input):

    lower_text = user_input.lower()

    # =========================
    # HCP NAME
    # =========================
    hcp_name = ""

    words = user_input.replace(",", "").split()

    for i, word in enumerate(words):

        if word.lower() == "dr":

            if i + 1 < len(words):
                hcp_name = "Dr " + words[i + 1]
                break

        elif word.lower().startswith("dr"):
            hcp_name = word
            break

    # =========================
    # INTERACTION TYPE
    # =========================
    interaction_type = "Meeting"

    if "call" in lower_text:
        interaction_type = "Call"

    elif "email" in lower_text:
        interaction_type = "Email"

    # =========================
    # SENTIMENT
    # =========================
    sentiment = ""

    if "positive" in lower_text:
        sentiment = "Positive"

    elif "negative" in lower_text:
        sentiment = "Negative"

    elif "neutral" in lower_text:
        sentiment = "Neutral"

    # =========================
    # MATERIALS
    # =========================
    materials = ""

    if "brochure" in lower_text:
        materials = "Brochure"

    elif "sample" in lower_text:
        materials = "Sample"

    elif "pdf" in lower_text:
        materials = "PDF"

    # =========================
    # ATTENDEES
    # =========================
    attendees = ""

    if "attendees" in lower_text:

        parts = lower_text.split("attendees")

        if len(parts) > 1:
            attendees = parts[1].strip()

    # =========================
    # TOPICS
    # =========================
    topics = ""

    if "discussed" in lower_text:

        start = lower_text.find("discussed")

        topic_text = user_input[start:]

        if "," in topic_text:
            topics = (
                topic_text
                .split(",")[0]
                .replace("discussed", "")
                .strip()
            )

    # =========================
    # DATE + TIME
    # =========================
    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    # =========================
    # OUTCOME
    # =========================
    outcome = "Interaction logged successfully"

    return {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "date": current_date,
        "time": current_time,
        "attendees": attendees,
        "topics": topics,
        "materials": materials,
        "sentiment": sentiment,
        "outcome": outcome
    }


# =========================
# GET ALL RECORDS
# =========================
def get_all_records():

    db = SessionLocal()

    records = db.query(Interaction).all()

    result = []

    for r in records:

        result.append({
            "hcp_name": r.hcp_name,
            "interaction_type": r.interaction_type,
            "date": r.date,
            "time": r.time,
            "attendees": r.attendees,
            "topics": r.topics,
            "materials": r.materials,
            "sentiment": r.sentiment,
            "outcome": r.outcome
        })

    db.close()

    return result


# =========================
# DELETE LAST RECORD
# =========================
def delete_last_record():

    db = SessionLocal()

    last_record = (
        db.query(Interaction)
        .order_by(Interaction.id.desc())
        .first()
    )

    if last_record:
        db.delete(last_record)
        db.commit()

    db.close()

    return "Last interaction deleted successfully"


# =========================
# EDIT LAST RECORD
# =========================
def edit_last_record(user_message):

    db = SessionLocal()

    last_record = (
        db.query(Interaction)
        .order_by(Interaction.id.desc())
        .first()
    )

    if not last_record:
        db.close()
        return "No record found"

    msg = user_message.lower()

    # Edit sentiment
    if "positive" in msg:
        last_record.sentiment = "Positive"

    elif "negative" in msg:
        last_record.sentiment = "Negative"

    elif "neutral" in msg:
        last_record.sentiment = "Neutral"

    # Edit topics
    if "topics to" in msg:

        parts = user_message.split("topics to")

        if len(parts) > 1:
            last_record.topics = parts[1].strip()

    db.commit()
    db.close()

    return "Last interaction updated successfully"


# =========================
# TOOL NODES
# =========================
def log_node(state):

    data = extract_data(state["message"])

    db = SessionLocal()

    new_interaction = Interaction(
        hcp_name=data["hcp_name"],
        interaction_type=data["interaction_type"],
        date=data["date"],
        time=data["time"],
        attendees=data["attendees"],
        topics=data["topics"],
        materials=data["materials"],
        sentiment=data["sentiment"],
        outcome=data["outcome"]
    )

    db.add(new_interaction)
    db.commit()
    db.close()

    return {
        "response": "Interaction logged successfully ✅",
        "form_data": data
    }


def show_node(state):

    records = get_all_records()

    return {
        "response": "All records fetched successfully",
        "records": records
    }


def delete_node(state):

    msg = delete_last_record()

    return {
        "response": msg
    }


def edit_node(state):

    msg = edit_last_record(state["message"])

    return {
        "response": msg
    }


def followup_node(state):

    return {
        "response": "Suggested follow-up: Schedule another meeting next week."
    }


# =========================
# ROUTER
# =========================
def router(state):

    msg = state["message"].lower()

    if "show all records" in msg:
        return "show"

    elif "delete last record" in msg:
        return "delete"

    elif "edit last record" in msg:
        return "edit"

    elif "followup" in msg:
        return "followup"

    else:
        return "log"


# =========================
# BUILD GRAPH
# =========================
graph = StateGraph(State)

graph.add_node("log", log_node)
graph.add_node("show", show_node)
graph.add_node("delete", delete_node)
graph.add_node("edit", edit_node)
graph.add_node("followup", followup_node)

graph.set_conditional_entry_point(
    router,
    {
        "log": "log",
        "show": "show",
        "delete": "delete",
        "edit": "edit",
        "followup": "followup"
    }
)

agent = graph.compile()


# =========================
# CHAT API
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    try:

        result = agent.invoke({
            "message": req.message
        })

        return result

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================
# HOME
# =========================
@app.get("/")
def home():

    return {
        "message": "Backend running 🚀"
    }