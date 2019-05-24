# Open Lewdness Engine

**Open Lewdness Engine** (or **OLE**) is a freely-available platform for creating modern flexible-narrative text adventures.  It was built from the ground up to be as easily moddable as possible, so creators can get right to making stories.  The base experience includes a pre-packaged storyline, but new storylines are easy to patch in via additional user-generated XML files.


## Structure
The game engine itself is written in the **Python** programming language, displayed using **PyGame**, and all of its content is stored in **XML files**.  When Open Lewdness Engine is activated, it first checks Settings.xml to load in basic game settings.  It then checks the **Stats** folder to find XML files which contain the lists of stats which characters will be using in the game.  Lastly, it loads your player character's save file from the **Saves** folder, before finally loading the first XML "story" file so that the game can begin.

This ability to load in any number of "stories" is the core utility of Open Lewdness Engine.  Items, narration, the location of image and sound files, even core gameplay elements like additional statistics or menus can be added directly to the game through a single XML file at run-time.  Many of these elements will need to be housed in separate directories elsewhere, but the story file binds them all together.

To prove this point, the base game which comes packaged with OLE is written entirely as XML-file "stories".

**Stories** have access to parts of the game such as the player character's statistics and the status of quests, plus a number of other things.  These are called **exposed variables**, and they can be used to create quests, immerse the player, and provide a dynamic experience.

All exposed variables exist in a single dictionary file, which is added to by an internal private process and an external public process.  The private process adds basic and universal variables, while the public process takes data from the XML files and adds them to the dictionary, so that user-generated variables can be patched in at run-time (like stories are).

The player character, NPC characters, and opponents all have profiles which are stored in another kind of XML file, a **character** file.  The player character's file is unique because it is a part of the save file, which includes other critical information pertaining to the game state, such as the status of quests and the current story page, which are to be loaded at startup.

**Stats** are the mechanical and statistical underpinnings of OLE.  While storytelling and player choice are important, they cannot be the only components of comprehensive RPG.  The basic stats of the core game are included within the Stats file as an XML document.  Stats are loaded into the game at run-time, so that anyone can add other stats to the game should they so choose.  When characters are instantiated, their save files expect certain stats to be present in the game.  If OLE cannot find a stat that a character should have, the stat will be ignored and the character will be created without that stat in play.  If extraneous stats are added in during start-up, a character will not take on any additional stats which are not outlined by their save file.


## Conventions
All "story" XML files are to be named without capital letters.  Only core files (such as Settings.xml) and save files may be capitalized.  This is for the sake of visual clarity.

"Stories" are to be placed in the Stories folder.  OpenLewdnessEngine will not look for stories anywhere else.

**Points** are the name given to bracketed words (words surrounded by "[" and "]") in XML stories.  These words are placeholders which OLE will swap out for something else.  A point must contain no spaces.  What a point is replaced by is largely up to the writer.

There are three types of Pages: **text**, **menu**, and **action**.  All Pages must have the attribute "type" equal to one of these three options.  This dictates how the Page data will be rendered.

The first Page in a Story file must have its "name" attribute equal to "start".  This is so the program always knows where to start.


## Opposition
When the player engages an NPC in a contest of some kind, the game switches to a different format.  In this mode, the player and the NPC oppose each other and take turns deciding how to act.

This system is used for **combat**, **conversation**, and **lewd encounters**.

This turn-based system is built around player and NPC skills, statistics, and items.  Each character must act respective to the others, and a focus is given to reacting to what the opposed character has just done by **chaining actions** for greater effect.  Some actions will be inaccessible to a character based upon what the opposed character has done; this goes for players and NPCs alike.