from fastapi import FastAPI
from models import MsgPayload
from config.config import APP_NAME
from config.logger import logger  # <-- import the logger
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os

# Set up OpenTelemetry tracing
resource = Resource(attributes={
    "service.name": APP_NAME,
    "service.environment": os.getenv("APP_ENV", "development"),
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Instrument FastAPI

app = FastAPI(title=APP_NAME)
FastAPIInstrumentor.instrument_app(app)
messages_list: dict[int, MsgPayload] = {}

@app.get("/")
def root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"message": "Hello"}

@app.get("/about")
def about() -> dict[str, str]:
    logger.info("About endpoint called")
    return {"message": "This is the about page."}

@app.post("/messages/{msg_name}/")
def add_msg(msg_name: str) -> dict[str, MsgPayload]:
    msg_id = max(messages_list.keys()) + 1 if messages_list else 0
    messages_list[msg_id] = MsgPayload(msg_id=msg_id, msg_name=msg_name)
    logger.info(f"Added message: msg_id={msg_id}, msg_name={msg_name}")
    return {"message": messages_list[msg_id]}

@app.get("/messages")
def message_items() -> dict[str, dict[int, MsgPayload]]:
    logger.info("Listed all messages")
    return {"messages:": messages_list}