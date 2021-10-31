init python:
    import os
    player_name = os.environ.get('username')
    osu = os.environ.get ('osname')

    e = Character(_("Eebee"), color="#00CC00")
    i = Character(_("Inventory"), color="#cccccc")
    o = Character(_("oleka"), color="#00CC00")
    b = Character(_("Blazer"), color="#00CC00")

    class Member:
        def __init__(self, name,
                     max_hp, cur_hp,
                     min_dmg, max_dmg
                     ):
            self.name = name
            self.max_hp = max_hp
            self.cur_hp = cur_hp
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg

        def update(self, anim, pos,
                   zoom=(1.0, 1.0), time=0.5):
            x, y = pos
            pos = Position(xalign=x, yalign=y)
            xzoom, yzoom = zoom
            tfms = Transform(xzoom=xzoom, yzoom=yzoom)
            trans = [Dissolve(time)]
            mem.dplay(anim, pos, tfms, trans)

        def dplay(self, anim, pos, tfms, trans):
            renpy.show(anim, at_list=[pos, tfms])
            for tran in trans:
                renpy.with_statement(tran)

        def show(self, anim_name, pos,
                   zoom=(1.0, 1.0), time=0.5):
            who = self.name.lower().replace('3', 'e').replace('0', 'o')
            anim = '%s %s' % (who, anim_name)
            self.update(anim, pos, zoom, time)

        def hide(self):
            renpy.hide('%s %s' % (self.name, 'disabled')) # Show character's turn is consumed

        def fainted(self):
            return (False if self.cur_hp > 0 else True)

        def say(self, msg):
            self.char(msg)

    class Party(Member):
        def __init__(self, name,
                     max_hp, cur_hp,
                     min_dmg, max_dmg,
                     char, fpos, bpos):
            super(Party, self).__init__(name, max_hp, cur_hp, min_dmg, max_dmg)
            self.char = char
            self.fpos = fpos
            self.bpos = bpos

        def getpos(self, stance):
            res = (0.0, 0.0)
            if (stance == 'back'):
                res = self.bpos
            elif (stance == 'front'):
                res = self.fpos
            return res

        def idle(self):
            anim_name = 'idle50' if self.cur_hp <= 50 else 'idle100'
            anim = '%s %s' % (self.name.lower(), anim_name)
            return anim

        def to(self, stance, anim='', zoom=(0.3, 0.3), time=0.5):
            anim = self.idle()
            pos = self.getpos(stance)
            self.update(anim, pos=pos, zoom=zoom, time=time)

        def setpos(self, fpos, bpos):
            self.fpos = fpos
            self.bpos = bpos

    # Define all possible party members here
    eebee  = Party("Eebee", 100, 100, 3, 5, e, [0.05, 0.78], [0.30, 0.78])
    oleka  = Party("Oleka", 100, 60, 5, 6, o, [-0.03, 0.8], [0.30, 0.80])
    blazer = Party("Blazer", 100, 49, 10, 15, b, [0.02, 0.5], [0.30, 0.80])

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
default healthcount = 100
default olekahealth = 100
