from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np

app = Flask(__name__)

#------------------
# home pagep
#------------------
