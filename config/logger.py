import logging
import os
import json
from opentelemetry import trace
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from datetime import datetime, timezone

os.makedirs("app_logs", exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "traceId": format(ctx.trace_id, "032x") if ctx.trace_id else "",
            "spanId": format(ctx.span_id, "016x") if ctx.span_id else "",
            "message": record.getMessage(),
        }
        # Add extra fields if present
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_record.update(record.extra_fields)
        return json.dumps(log_record)

logger = logging.getLogger("fastapi-otel")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("app_logs/application.log")
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
LoggingInstrumentor().instrument(set_logging_format=False)