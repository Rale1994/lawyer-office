import os
import secrets
from flask import current_app


def save_document(form_document):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_document.filename)
    document_fn = random_hex + f_ext
    document_path = os.path.join(current_app.root_path, 'static/documents', document_fn)

    form_document.save(document_path)

    return document_fn
