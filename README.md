Dispatch
========================

Dispatch is an application and file launcher for Linux. 
It is still **a work in progress** but should be mostly usable at this point.

It was created because I could not find a launcher that would index all of my files without slowing down... but it does a little more than just fix that.

Features
-------------------------
- Indexes applications (including command line applications) and files and directories in your home directory
- Opens on the left of the screen, so that it can stay out of your way... opposed to opening front and center.
- Actions can be preformed on matches (which are themselves actions). To see the possible actions that can be preformed on a match type `/` when selecting a match
- Supports navigating directories
- Most used matches come to the top, so that you can later just type something and press enter without looking
- UI is customizable (dispatch/ui/style.css)
- Live results can be returned for queries (plugins required)
- Plugin system is simple

Notes
------------------------------------
- When initially starting the program it may lag a little. This is because it is loading plugin data and populating the cache.
- Only the top 25 matches are shown for a given query. This should not be a problem because the most used matches come to the top of the list. So once you select it for the first time (by a more specific query) it should come to the top of the list for future less specific queries.
	- you can change this in (dispatch/search.py the RESULT_LIMIT) but note that this will slow things down


Usage
------------------------
- `Ctrl-Space` shows the window
- `enter` on a match opens it (eg. opens that application, file or directory)
- `/` on a match shows actions that can be preformed on that match (e.g. `/` on a directory match shows files in that directory)
- `F6` re-indexes everything


Stuff that needs to be done
-------------------------------------
- Indexes should be updated automatically without having to press `F6`
- Loading data from plugins and populating the cache should be done asynchronously
	- currently this results in an initial lag
- Memory usage should be decreased


Plugins
-------------------------
- There are two main concepts:
	- **Actions** 
		- Are the results that are shown when you type in something i.e. the matches
		- They do something when you press enter on them
	- **Operators**
		- Responsible for returning actions
		- Operators either:
			1. operate on an existing action. These actions are shown when you press `/` on an action. e.g. AppArgumentOperator requires an AppAction or CmdAction to attach arguments to.
			2. operate on no other action (None). These actions are shown when you search by default. e.g. FileOperator does not require an action, when you being searching the results of this operator are available.
- For writing a plugin look at the examples in the plugins directory (dispatch/plugins) and look at the plugin api (dispatch/api.py)
- Some things that you can do or don't have to do
	- return live results based on the current query
	- for static results searching is done internally and not in the plugin, so no need to write code to search
	- Actions can be attached to other actions e.g. create an operator that operates on a TextAction and returns a PrintAction that prints the text on the screen
