import json
from loguru import logger


def json_formatter(record):
    log_record = {
        "message": record["message"],
        "level": record["level"].name,
        "time": record["time"].isoformat()
    }

    extra = record.get("extra", {})
    if "req" in extra:
        log_record["req"] = extra["req"]
    if "res" in extra:
        log_record["res"] = extra["res"]

    if record["exception"]:
        log_record["err"] = str(record["exception"])

    return json.dumps(log_record)


logger.remove()
logger.add(lambda msg: print(json_formatter(msg.record)), serialize=False)
logger.disable("uvicorn.access")