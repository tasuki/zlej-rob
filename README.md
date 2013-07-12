# Zlej Rob

A semi-intelligent solver for [RoboZZle]. See [zlejrob's profile] &ndash; currently
in [top 100] out of 10,000+ players.

[RoboZZle]:          http://robozzle.com/
[top 100]:           http://robozzle.com/scoreboard.aspx
[zlejrob's profile]: http://robozzle.com/user.aspx?name=zlejrob

[![Build Status](https://travis-ci.org/tasuk/zlej-rob.png?branch=master)](https://travis-ci.org/tasuk/zlej-rob)

## Install

You'll need `python 3` and `pip` installed. After that, install project
dependencies with:

    pip install -r requirements.txt --use-mirrors

> Watch out: `pip` refers to Python 2 version of pip on certain systems
> (Ubuntu). You might need to specify the version explicitly by calling e.g.
> `pip-3.3` instead.

## Use

The following is a sample of how to run zlejrob. Not knowing optimal solver
configuration myself, I'll leave that as an exercise for the reader:

    from zlejrob import Client, Runner, Zlo
    
    client = Client({
        'name': 'name',   
        'pass': 'password',   
    })
    
    solver_config = {
        'star_score': int,
        'reached_score': int,
        'length_penalty': int,
        'degeneration': float,
        'mutability': int,
        'offsprings': int,
        'survivors': int,
        'generation_limit': int,        
    }
    
    zlo = Zlo(client, Runner(max_steps=100), solver_config)
    zlo.fetch_solve_submit(27) # fetch and solve one puzzle
    zlo.solve_unsolved_puzzles() # run through the default campaign

*Please do not submit zlejrob solutions as your own.*

## Contribute

A prerequisite for running the test suite is putting your robozzle.com login
details in `zlejrob/config.py`. The test suite can be run with:

    python -m unittest discover

> Watch out: `python` refers to Python 3, on certain systems (Ubuntu), you'll
> need to specify the version explicitly by using `python3` instead.
