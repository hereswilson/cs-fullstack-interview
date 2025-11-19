def encrypt_ssn(ssn):
    return ssn


def flatten_marshmallow_errors(errors, parent_key=""):
    flattened = []
    for field, messages in errors.items():
        key = f"{parent_key}.{field}" if parent_key else field
        if isinstance(messages, dict):
            flattened.extend(flatten_marshmallow_errors(messages, key))
        else:
            for msg in messages:
                flattened.append({"field": key, "message": msg})
    return flattened
