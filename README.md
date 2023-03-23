## Customs Inspector

Customs Inspector is a Python tool that hooks into Poetry's package management system 
to allow for manual auditing of package changes during updates. 
When you run ``poetry update``, Customs Inspector will open a browser with a GitHub diff like view, requesting you to confirm or reject the update before proceeding.

## Note:
TESTED ONLY ON Poetry ``v1.4.x``  
This is a proof of concept. Poetry **explicitly** says to not use the plugin system to modify existing commands.
If this is something that is considered valuable, I would love to discuss this with Poetry's authors to potentially integrate it.

### Why?
Developers are lazy, we'd rather not audit source code...  
Well, we cannot afford that anymore.
I am also not interested in the snake oil automated analysis companies are selling (for now).

What if auditing was really easy to do so?  
What if, we could harness the community's collective effort to find malicious packages?

### Usage
See: [how to install plugins](https://python-poetry.org/docs/master/plugins/#using-plugins)  
```
poetry update
```
### Upcoming:
- [ ] Increase speed
- [ ] Add language server support to make auditing even easier
- [ ] Add file filtering, to hide test folders, for example
- [ ] Add rules for quick auditing, for example when new sensitive APIs are used (``socket, os, sys``)

### Contributions
Feedback, contributions and suggestions welcome.

### License
GPL-3.0
