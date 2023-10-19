#!/usr/bin/python3
"""
file: index.py
Desc: A module which starts the web app
Authors: Teklemariam, Dawit Mulugeta Tdege, and kidus kinde
Date Created: Sep 18, 2023
"""
from front_end import app

if __name__ == "__main__":
    """Main Function"""
    app.run(host='127.0.0.1', port=5000, debug=True)
