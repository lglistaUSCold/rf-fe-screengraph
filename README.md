# rf-fe-screengraph
This python script will comb through a directory for cpp files and make connections between screens by searching for lines like
`currentScreen = screenName` or `currentScreen = sessionData::ms_previousScreen`

## Dependencies
This script is run with `python3`. There are no external dependencies for the python script

### GraphViz - https://graphviz.org/
If you want to make use of the output, you will want to install `Graphviz`. The command line tool it installs is named `dot`

Mac - https://formulae.brew.sh/formula/graphviz

## How to run
### Quickstart
These 2 commands run back to back will produce a file named `out.svg` that you can open in your web browser. You could also pipe the python script output to `dot`
```
python3 generate_dot_file.py <dir>/USCS-RF-FE >> rffe.dot
dot -Tsvg rffe.dot >> out.svg
```

### Other ways to run
You could run this command with `<dir>/USCS-RF-FE/shipping_taskmaster/Task_Picking` if you only wanted the graph in the Task_Picking Module. However, you will need to edit 
`validate_links()` to always return `False`. This script will still complain, but `dot` will be able to generate the graph without any issues

Additionally, you could change the `dot` output file format. See https://graphviz.org/doc/info/command.html

## Further Development
https://graphviz.org/doc/info/lang.html

https://www.graphviz.org/pdf/dotguide.pdf

1. We can add colors to the nodes to organize them by module
2. We can add names to the edges by parsing the cpp files further (e.g. naming an edge by the function key required to cause the screen change)
3. Option to remove ms_previousScreen node
4. Find ALL ways that screens can be changed (there are some indirect ways to do it, such as `m_pCommonServices->returnToPreviousScreen()`
