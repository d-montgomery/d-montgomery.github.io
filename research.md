---
title: Research
permalink: /research/
layout: single
author_profile: true
---

## Overview of Research
My research applies computational mathematics to advance the understanding of reactive flows across a range of scientific and engineering applications, including sustainable aviation fuel combustion, CO₂ desublimation for carbon capture, and blood clot formation. This work involves the development and maintenance of open-source software in C++ and Python to enable high-fidelity simulation of complex multiphysics systems.

Selected examples below provide visual demonstrations of these research efforts.

## Heterogeneous Nucleation of CO₂ in Carbon Capture Systems
Conference presentation from the Rocky Mountain Fluid Mechanics Symposium describing collaborative work with [Carbon America](https://www.carbonamerica.com/) on modeling heterogeneous nucleation processes in carbon capture systems ([NLR/PR-2C00-96067](https://doi.org/10.2172/3015021)).

[📄 View PDF](https://docs.nrel.gov/docs/fy26osti/96067.pdf){: .btn .btn--primary target="_blank"}


## Hemostasis in a Microfluidic Device
Using the **clotFoam** framework, we simulate platelet-mediated coagulation across a range of physiologically relevant geometries. This example models hemostasis following an extravascular injury within an *in vitro* microfluidic device. Blood enters through the right channel while a buffer fluid flows through the left channel at a lower rate, driving blood into a horizontal channel coated with tissue factor and collagen to initiate platelet adhesion and coagulation.
- Relevant publication: [doi:10.1016/j.softx.2023.101483](https://doi.org/10.1016/j.softx.2023.101483) 
- GitHub project: [github.com/d-montgomery/clotFoam/tutorials/Hjunction3D](https://github.com/d-montgomery/clotFoam/tree/main/tutorials/Hjunction3D)
{% include video id="Kg1CA9HNLQ4" provider="youtube" %}


## Thrombosis
This simulation demonstrates thrombus formation resulting from an intravascular injury using the clotFoam software framework, highlighting the model’s ability to capture complex clot growth dynamics under flow conditions.
- Relevant publication: [doi:10.1016/j.softx.2023.101483](https://doi.org/10.1016/j.softx.2023.101483) 
- GitHub project: [github.com/d-montgomery/clotFoam/tutorials/rectangle2D](https://github.com/d-montgomery/clotFoam/tree/main/tutorials/rectangle2D) 
{% include video id="edcutJePIzk" provider="youtube" %}