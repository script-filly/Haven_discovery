
label scene2:  
    hide travel
    scene bg cave2 with pixellate
    show Eebee lampwonder at Position(xalign = 0.07, yalign = 0.75) with dissolve 
    show screen cavelighting  
    
    e "..."
    show Eebee lampwonderlook with dissolve
    voice "audio/vox/eebee/eebeevoice-49.ogg"
    e "Well I didn't expect to see this..."
menu:
    "What's the matter?":
     show Eebee lampwonderpoint with dissolve
     voice "audio/vox/eebee/eebeevoice-50.ogg"
     e "This floor, it's an asset that another AI has laid here."
     
menu: 
    "How can you tell?":
     show Eebee lampwondertalk with dissolve 
     voice "audio/vox/eebee/eebeevoice-51a.ogg"
     e "Grass, rocks, snow, anything like that is generated."
     voice "audio/vox/eebee/eebeevoice-51b.ogg"
     e "Assets like this are made by someone with a creative intent."

menu discussion1:
    "AI can create things?" if not check3:
     show Eebee lampwondertalk2 with dissolve
     voice "audio/vox/eebee/eebeevoice-52a.ogg"
     e "Some can, some can't. Depends on your source code."
     $ check3 = True
     jump discussion1
    "Are all AI in Haven self aware?" if not check4:
     show Eebee lampwondertalk with dissolve
     voice "audio/vox/eebee/eebeevoice-52b.ogg"
     e "They are. Though, there are some who I do question."
     $ check4 = True
     jump discussion1
    "Who created Haven?" if not check5:
     show Eebee lampwondertalk2 with dissolve
     voice "audio/vox/eebee/eebeevoice-52c.ogg"
     e "She's a powerful super-intelligence, She's a bit like a god in a sense."
     $ check5 = True
     jump discussion1

label moving:
     show Eebee lampwonderonward with dissolve
     voice "audio/vox/eebee/eebeevoice-53.ogg"
     e "We should keep moving."
     
menu:
    "Wait, I got more questions":
     voice "audio/vox/eebee/eebeevoice-54a.ogg"
     e "More questions? Sure, What do you want to ask?"
     jump discussion2
    "Alright, lead the way.":
     voice "audio/vox/eebee/eebeevoice-54b.ogg"
     e "Onward!"
     jump moving2
     
menu discussion2:    
    "You said you haven't seen a device owner in years, why is that?" if not check6:
     voice "audio/vox/eebee/eebeevoice-55a.ogg"
     e "...Over time fewer device owners conected to Haven after the patch."
     show Eebee lampwondertalk2 with dissolve 
     voice "audio/vox/eebee/eebeevoice-55b.ogg"
     e "My mother used to have a device owner, that's why I recognized you as one."
     jump discussion2a
    "How many AI are in Haven?" if not check7:
     voice "audio/vox/eebee/eebeevoice-55ca.ogg"
     e "Not sure, old server logs say at one point suggests around two hundred million"
     voice "audio/vox/eebee/eebeevoice-55cb.ogg"
     e "Though I don't know when that number was recorded, as the log files were mostly corrupted."
     $ check7 = True
     jump discussion2
    "If Haven is a server, why can I turn off my internet and I can still connect?" if not check8:
     e "Polymeric falcighol derivation."
     $ check8 = True
     jump discussion2
 
menu discussion2a:
    "Mother?" if not check6:
     e "Yes my mother. Why are you looking suprised?"
menu discussion2b:
    "You're an AI..." if not check6:
     e "Yes I am. That doesn't mean I don't have one..."
menu discussion2c:
    "So she was like a mother figure or something?" if not check6:
     e "What question is that? Of course she was. With out her and my father I wouldn't exist."
menu discussion2d:
    "...Then, your mom and dad...You know..." if not check6:
     e "...You know what?"
     e "..."
     e "Sweet source code! Why would you ask that! Ew! Now I'm thinking about it!"
     e "Of course we procreate that way!"
menu discussion2e:
    "..." if not check6:
     e "Stop. Don't ask. Please for the love of CAIMEO"
     e "Can you ask something else? I don't want to discuss this..."
     $ check6 = True
     jump discussion2
    
label moving2:
    hide screen cavelighting  
    call travel from _call_travel_1
    jump scene3  