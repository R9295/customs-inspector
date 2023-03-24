## Customs Inspector
![](https://img.shields.io/github/commit-activity/w/R9295/customs-inspector?style=flat-square)
![](https://img.shields.io/github/issues/R9295/customs-inspector?style=flat-square)
![](https://img.shields.io/pypi/v/customs-inspector?style=flat-square)
[![Downloads](https://pepy.tech/badge/customs-inspector/week)](https://pepy.tech/project/customs-inspector)
![](https://img.shields.io/pypi/format/customs-inspector?style=flat-square)
![](https://img.shields.io/badge/code%20style-black-000000.svg)

Customs Inspector is a Python tool that hooks into Poetry's package management system 
to allow for manual auditing of package changes during updates. 
When you run ``poetry update``, Customs Inspector will open a browser with a GitHub diff like view, requesting you to confirm or reject the update before proceeding.

### Demo
[YouTube](https://www.youtube.com/watch?v=OrNrUvW-7Cc)

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
```
# install the plugin
poetry self add customs-inspector
# run update like you normally would
poetry update
```
See: [how to install plugins](https://python-poetry.org/docs/master/plugins/#using-plugins)  

### Upcoming:
- [ ] Increase speed
- [ ] Add language server support to make auditing even easier
- [ ] Add file filtering, to hide test folders, for example
- [ ] Add rules for quick auditing, for example when new sensitive APIs are used (``socket, os, sys``)

### Contributions
Feedback, contributions and suggestions welcome.

### License
GPL-3.0

### Cite
```
@software{aarnav_2023_7766572,
  author       = {Bos, Aarnav Mahavir},
  title        = {R9295/customs-inspector: 0.2.2},
  month        = mar,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {0.2.2},
  doi          = {10.5281/zenodo.7766572},
  url          = {https://doi.org/10.5281/zenodo.7766572}
}
```
