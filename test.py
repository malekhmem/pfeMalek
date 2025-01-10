import torch
print(torch.__version__)
print("cuda is available ",torch.cuda.is_available())
print("cuda version " , torch.version.cuda)
print("gpu name ", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no gpu")


# test_flask_import.py
try:
    import flask
    print("Flask importé avec succès!")
except ImportError as e:
    print(f"Erreur d'importation de Flask: {e}")

import sys
print(sys.executable)
try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, session
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager, login_user, login_required, logout_user, current_user
    print("Tous les modules Flask sont importés avec succès !")
except ImportError as e:
    print("Erreur d'importation :", e)


import torch
import transformers
import AutoGPTQ

print("AutoGPTQ est installé avec succès !")
