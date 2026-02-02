---
title: Publications
permalink: /publications/
layout: single
author_profile: true
---

{% assign pubs = site.data.publications | default: empty %}

{% if pubs == empty %}
**Publications list is not generated yet.**
{% else %}

{% for p in pubs %}
- **{{ p.title }}**{% if p.year %} ({{ p.year }}){% endif %}{% if p.venue %}. *{{ p.venue }}*{% endif %}{% if p.doi %}. DOI: [{{ p.doi }}](https://doi.org/{{ p.doi }}){% endif %}
{% endfor %}

{% endif %}
