# SWGOH Mod Squad App

This app helps modding of SWGOH teams as opposed to individual game characters. This document describes the SWGOH game and helps specify the database requirements. The database requirements are defined in entity relation diagrams that form the basis of the database design.

## Game Play

SWGOH players use teams of characters to progress through the game. Game play in SWGOH is divided into a series of holotables that are presented on the front screen of the game. Each holotable hosts either events or shops. Players use their teams of characters within the events to battle other teams. Events have different levels of persistence, i.e. always present, guild driven, and calendar driven.

Teams in SWGOH are comprised of different characters. The number of characters on a team is usually 3 or 5, depending on the event. SWGOH characters belong to different factions and teams generally consist of characters who belong to the same faction. Characters also have different attributes such as speed and strength that depend on the character's level, gear, and mods.

A SWGOH character's level is controlled by the number of character shards that have been applied. There are seven levels and higher levels require a greater number of shards. Character shards can be obtained as rewards from defeating teams during events.

Describe gear levels.

The third way a character can increase their attributes is by equipping them with mods. Unlike gear, mods can be added or removed from characters at will, to fine-tune character's attributes.

Unfortunately, there many sources of mod suggestions. Players are often overwhelmed by these choices and this document will try to tabulate some of the more common mod suggestions.