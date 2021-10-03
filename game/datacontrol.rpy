init python:
    import os
    player_name = os.environ.get('username')
    osu = os.environ.get ('osname')

python:
    if affectioncount <= 0:
     affectioncount = 0
    if olekaaffection <= 0:
     olekaaffection = 0
## Misc ##

# AI Choice Check - Things AI decides themselves
default forgiveplayer = False


# Story checks
default lighton = False
default bagactive = False
default bagfound = False
default gunfound = False
default okelajoined = True
default blazerjoined = True
default bookcount = 0
default cryptocount = 0
default affectioncount = 5
default olekaaffection = 5
default healthcount = 100
default olekahealth = 60
default blazerhealth = 49
#Manual data checks- will recode once a better way is found
default check1 = False
default check2 = False
default check3 = False
default check4 = False
default check5 = False
default check6 = False
default check7 = False
default check8 = False
