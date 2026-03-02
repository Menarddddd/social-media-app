from sqlalchemy.exc import IntegrityError


def get_constraint_name(e: IntegrityError):
    msg = str(e.orig)
    if "Key (" in msg:
        start = msg.find("Key (") + 5
        end = msg.find(")", start)

        return msg[start:end].strip()

    return "unknown_field"
