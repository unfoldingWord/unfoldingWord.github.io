---
layout: default
title: Unlocked Dynamic Bible
permalink: /udb/index.html
header_image_layout: icon
header_image: icon-udb.png
credits: >
  The "Unlocked Dynamic Bible" is a revision of "[Translation for Translators](https://git.door43.org/Door43/T4T)" (by Ellis W. Deibler Jr. made available under a [Creative Commons Attribution-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-sa/4.0) license), designed by unfoldingWord and revised by the [Door43 World Missions Community](https://door43.org/). It is made available under a [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) license.
---

{% assign y = 'udb' | get_by_dc_id %}
<p>{{ y.dublin_core.description }}</p>
<p>The Unlocked Dynamic Bible is intended to be used together with the [Unlocked Literal Bible][ulb] to provide a more robust view of both the form and function of the original texts.</p>

<ul>
 <li>Version: {{ y.dublin_core.version }}</li>
 <li>Release Date: {{ y.dublin_core.issued | date: "%e %B %y" }}</li>
 <li>Status: {% case y.checking.checking_level %}
{% when '3' %}Stable {% else %}In progress
{% endcase %}</li>
</ul>

<div class="text-center">
 <p>
  <a class="btn btn-dark btn-sm" href="https://cdn.door43.org/en/{{ y.dublin_core.identifier }}/v{{ y.dublin_core.version }}/pdf/en_{{ y.dublin_core.identifier }}_v{{ y.dublin_core.version }}.pdf" title="{{ y.dublin_core.identifier | upcase }} Version {{ y.dublin_core.version }} PDF">
   <i class="fa fa-file-pdf-o"></i> Download PDF
  </a>
  <a class="btn btn-dark btn-sm" href="https://door43.org/u/Door43-Catalog/en_udb/ade6251820/" title="{{ y.dublin_core.identifier | upcase }} Version {{ y.dublin_core.version }} Web">
   <i class="fa fa-globe"></i> View on the Web
  </a>
  <a class="btn btn-dark btn-sm" href="{{ y.dublin_core.url }}" title="{{ y.dublin_core.identifier | upcase }} Version {{ y.dublin_core.version }} Source">
   <i class="fa fa-archive"></i> View Source
  </a>
</p>
</div>

<hr>
<p>Or, <a data-toggle="collapse" href="#collapseBooks" aria-expanded="false" aria-controls="collapseBooks">browse by book</a>.
</p>

<div class="collapse" id="collapseBooks">
<table class="table table-striped table-responsive">
 <tbody>
  <tr>
   <td>Old Testament</td>
   <td><a href="https://cdn.door43.org/en/{{ y.dublin_core.identifier }}/v{{ y.dublin_core.version }}/pdf/en_{{ y.dublin_core.identifier }}_v{{ y.dublin_core.version }}_ot.pdf" title="{{ proj.title }} PDF"><i class="fa fa-file-pdf-o"></i> Download PDF</a></td>
   <td><a href="https://door43.org/u/Door43-Catalog/en_udb/ade6251820/01-GEN.html" title="{{ proj.title }} Web"><i class="fa fa-globe"></i> View on the Web</a></td>
  </tr>
  <tr>
   <td>New Testament</td>
   <td><a href="https://cdn.door43.org/en/{{ y.dublin_core.identifier }}/v{{ y.dublin_core.version }}/pdf/en_{{ y.dublin_core.identifier }}_v{{ y.dublin_core.version }}_nt.pdf" title="{{ proj.title }} PDF"><i class="fa fa-file-pdf-o"></i> Download PDF</a></td>
   <td><a href="https://door43.org/u/Door43-Catalog/en_udb/ade6251820/41-MAT.html" title="{{ proj.title }} Web"><i class="fa fa-globe"></i> View on the Web</a></td>
  </tr>
  {% for proj in y.projects %}
  {% capture usfm_name %}{{ proj.path | remove: ".usfm" | remove: "./" }}{% endcapture %}
  <tr>
   <td>{{ proj.title }}</td>
   <td><a href="https://cdn.door43.org/en/{{ y.dublin_core.identifier }}/v{{ y.dublin_core.version }}/pdf/en_{{ y.dublin_core.identifier }}_{{ usfm_name }}_v{{ y.dublin_core.version }}.pdf" title="{{ proj.title }} PDF"><i class="fa fa-file-pdf-o"></i> Download PDF</a></td>
   <td><a href="https://door43.org/u/Door43-Catalog/en_udb/ade6251820/{{ usfm_name }}.html" title="{{ proj.title }} Web"><i class="fa fa-globe"></i> View on the Web</a></td>
  </tr>
  {% endfor %}
 </tbody>
</table>
</div>

[ulb]: {{ '/ulb' | prepend: site.baseurl }} "Unlocked Literal Bible"
