init python:
    import os
    player_name = os.environ.get('username')
    osu = os.environ.get ('osname')

    # Define Member
    class Member:
        def __init__(self, name, max_hp, cur_hp, min_dmg, max_dmg):
            self.name = name
            self.max_hp = max_hp
            self.cur_hp = cur_hp
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg

        def display(self, anim, xalign=0.05, yalign=0.8):
            pos = Position(xalign=xalign, yalign=yalign)
            trans = Dissolve(0.5)
            renpy.show(anim, at_list=[pos])
            renpy.with_statement(trans)

        # Show status of party members
        def show_status(self, xalign, yalign=0.78, anim_name=''):
            if anim_name is '':
                anim_name = 'idle50' if self.cur_hp <= 50 else 'idle100'
            who = self.name.lower()
            anim = '%s %s' % (who, anim_name)
            self.display(anim, xalign, yalign)

        def fainted(self):
            return (False if self.cur_hp > 0 else True)

    eebee = Member("Eebee", 100, 100, 3, 5)
    oleka = Member("Oleka", 100, 60, 5, 6)

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
