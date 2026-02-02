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

<ol reversed>
{% for pub in site.data.publications %}
  <li>

    {% if pub.authors %}
      {% assign authors = pub.authors | join: ", " 
        | replace: "David Montgomery", "<strong>David Montgomery</strong>"
        | replace: "D. Montgomery", "<strong>D. Montgomery</strong>" %}
      {{ authors }}.<br>
    {% endif %}

    {% if pub.title %}
    <em>{{ pub.title }}</em>,
    {% endif %}

    {% if pub.venue %}
      {{ pub.venue }},
    {% endif %}
    {{ pub.year }}, 

    {% if pub.doi %}
    <a href="https://doi.org/{{ pub.doi }}" target="_blank">
        doi:{{ pub.doi }}.
    </a>
    {% endif %}

  </li>
{% endfor %}
</ol>

{% endif %}
