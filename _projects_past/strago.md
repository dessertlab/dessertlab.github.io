---
title: STRAGO-WSN
subtitle:  Strategies for the Design, Configuration, and Validation of QoS-critical Wireless Sensor Networks

description: |

people:
  - domenico-cotroneo

proj-roles:
  - principal-investigator

image:
layout: project
no-link: false
last-updated: 2023-04-01
---

### Subjects
Strago s.r.l. and CINI consortium.

### Description

The project aim is the study, the analysis, and the sperimentation of strategies for the development of QoS-critical Wireless Sensor Networks (WSNs). The quality of such networks is an attribute composed by several sub-attributes (e.g. dependability, scalability, self-configurability, battery consumption, and maintainability) which are dependent on application and environmental requirements. Those attributes will be evaluated on the field on a WSN prototype.
Strago s.r.l. sponsors the CINI consortium with 2 annual fellowship grants for this project. The study and research activity take place at both the CINI-ITEM laboratory at Naples, and the Strago's research laboratory at Pozzuoli (Naples).
The CINI-ITEM laboratory (Naples) provides Strago s.r.l. with the scientific and the technological support, in particular i) to define in detail the software requirements of WSNs for applications which are of interest for Strago s.r.l, ii) to define strategies for software development for WSNs, and iii) for the know-how acquisition and the technology transfer useful for the development of a precompetitive prototype.

### Details and results
The project lasted one year. It started in December 2005 and ended in September 2006. It evolved according to four phases, as evidenced in the following:

- Phase 0: Acquisition and study of a WSN kit.
	- Description: During this short phase the main available technologies for WSNs were analyzed with the objective to choose a proper kit for further investigations, conducted in the subsequent phases. Phase end: 15 December 2005.
	- Outputs: comparison of available kits and acquisition of a Mote KIT composed by several mote processor boards and sensors, one programming board, and one sink node (stargate).
- Phase 1: Analysis and study of WSNs' development platforms.
	- Description: The aim of this phase was the detailed analysis of the main enabling technologies for WSNs, along with the study of the operating systems and development platforms, specifically embedded linux and TinyOS. Phase end: 16 January 2006.
	- Outputs: a deliverable summarizing the main characteristics of TinyOS and Embedded Linux, along with the description and examples of the application development cycle for both the platforms.
- Phase 2: Design and implementation of a WSN prototype.
	- Description: Based on the studies performed in previuos phase, and exploiting the acquired Mote development kit, a WSN prototype was developed by the CINI-ITEM, according to Strago's needs. In particular, the prototype was oriented to the monitoring of civil structures and had to be able to i) gathering acceleration measures from sensors, ii) displaying the gathered measures in a real--time fashion on a PC (linked with the sink node) in a graphical format, and iii) displaying the same measures in a real-time fashion from mobile devices (i.e., smart phones). Phase end: 13 June 2006.
	- Outputs: 1) a deliverable summarizing the design and implmentation choices of the prototype, including the installation notes. 2) the prototype itself, composed by five sensor nodes (3 mica2 and 2 mica2dot), one sink node, one server node for data registration, one PC and three mobile phones for data displaying. 3) a pubblication on the requirements of WSNs for structural monitoring, published at the 2006 Intl. Workshop on Applied Software Reilability (WASR), held in conjunction with the 2006 IEEE international conference on Dependable Systems and Networks (DSN'06), and presented on June 2006.
- Phase 3: Analysis of the reliability of a real world Strago's system, and definition of a novel sink node (R-URGD).
	- Description: The first period of this last phase was concerned with the study of a really deployed Strago's wired sensor network, with the objective of measuring its reliability and identifying its dependability bottlenecks. Since it appeared clear that the sink node, namely URGD (Unità di Raccolta e Gestione Dati), represented the main dependability bottleneck of the whole network, the very last phase of the activity was concerned with the definition and implementation of a prototype of a novel sink node, called Reliable URGD (R-URGD), able to automatically detecting and reporting common system failures. Phase end: 30 September 2006.
	- Outputs: 1) a deliverable reporting the reliability study of the Strago's system, the software requirements specification and the high-level design of the R-URGD. 2) the R-URGD software prototype, deployed on the same hardware of the previous URGD version, and linked with actual Strago's sensors (UADs).
