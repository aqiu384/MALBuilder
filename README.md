# MALBuilder
UIUC CS428 Software Engineering II Spring 2015 repository for MALBuilder

# Contributors
Allen Qiu
Andrew Nguyen
David Tang
Zane Nicholson
Harlan Cao
Jaily Zeng

# Description
Both Japanese animation (anime) producers and consumers require a tool to keep track of anime titles regular watchers have enjoyed, both to help the ordinary fan determine which show to watch next as well as provide feedback to the industry on which genres are most popular, and therefore more profitable. However, current online anime indices like MyAnimeList (MAL) require many transactions on the user’s part to update said lists, discouraging many potential users from updating their MAL and providing better feedback for titles on a regular basis. Our proposed application, MALBuilder, would provide a much simpler interface for modifying anime watchlists in bulk and synchronizing them with the users main MAL. MALBuilder would help regular anime watchers complete an accurate MAL as well as encourage them to update their watchlists more frequently, providing better feedback and watch demographics on whole.

# Setup
1. Get Python 3.4
2. Install all dependencies from requirements.txt
3. Download and start postgres with databases named 'malb-prod' and 'malb-test' with owner 'dev' password 'uiuc'
4. Run inittestdata.py to populate database with test data
5. Run run.py to start MALB

# Documentation
Overview: See project_documentation.pdf for general project overview.
Code: See http://www.stack.nl/~dimitri/doxygen/manual/docblocks.html#pythonblocks to convert embedded docstrings to HTML. Target the src directory.