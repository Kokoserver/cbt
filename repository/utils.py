import json
import pandas as pd
from fastapi.responses import JSONResponse


def get_user_claims(get_user_details):
    return json.loads(get_user_details)


def convert_csv_to_list_dict(csv_file, model):
    df = pd.read_csv(csv_file.file)
    return [model(**row.to_dict()).dict() for index, row in df.iterrows()]


def convert_to_list_dict__to_excel(listOfDict):
    return pd.DataFrame.from_dict(listOfDict)

    # return [model(**row.to_dict()).dict() for index, row in df.iterrows()]


def get_message(root: str, fields: list, error_message: str, return_message=None):
    return_message = return_message or {}

    if root not in return_message:
        return_message[root] = {}

    for i, field in enumerate(fields):
        if len(fields) == 1:
            return_message[root].update({field: error_message})
        else:
            new_fields = fields.copy()
            del new_fields[i]
            response = get_message(
                root=field,
                fields=new_fields,
                error_message=error_message,
                return_message=return_message[root],
            )
            return_message[root].update(response)
            break

    return return_message


async def validation_bad_request_exception_handler(request, exc):
    message = {}
    for x in exc.errors():
        fields = [entry for entry in x["loc"] if entry != "body"]

        if len(fields) == 0:
            message.update({"error": "invalid request"})
        elif len(fields) == 1:
            message.update({fields[0]: x["msg"]})
        else:
            # for dict / list with errors inside it
            field_root = fields[0]
            del fields[0]

            message = get_message(
                root=field_root,
                fields=fields,
                error_message=x["msg"],
                return_message=message,
            )

    return JSONResponse(
        status_code=400,
        content={
            "message": message,
        },
    )
