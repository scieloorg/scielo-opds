=============================
OPDS support for SciELO Books
=============================

This is an implementation of an Open Publication Distribution System (OPDS_)
catalog for the SciELO Books application.

.. _OPDS: http://opds-spec.org/

---------
Objective
---------

To allow a user with an OPDS compatible e-reader application or device to
browse the catalog of books available through the SciELO Books portal.


OPDS compatible E-reader apps
=============================

- Aldiko (Android): http://www.aldiko.com/

- Bluefire (Android, iOS): http://www.bluefirereader.com/

- FBreader (Android, Symbian, Meego etc.): http://www.fbreader.org/
 
- Stanza (acquired by Amazon.com and discontinued)


Roadmap
=======

- *ENT-01* Catalog Root (last books, editors, alphabetycal) [1]_
- *ENT-03* Partial Catalog Entry (acquisition feed) [1]_
- *ENT-04* Complete Catalog Entry (with pagination) [1]_
- *ENT-05* Scielo webservice integration for Catalog Root/Entry
- *ENT-06* Scielo webservice integration for Catalog Entry
- *ENT-07* Compression and caching support (application side)
- *ENT-08* Definition of deploy and configuration process


.. [1] with fixtures provided by Scielo.